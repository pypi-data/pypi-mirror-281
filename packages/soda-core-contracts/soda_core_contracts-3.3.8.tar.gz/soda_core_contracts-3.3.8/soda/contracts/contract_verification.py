from __future__ import annotations

from typing import Iterator

from soda.contracts.contract import Contract, ContractResult
from soda.contracts.impl.contract_verification_impl import (
    FileVerificationWarehouse,
    SparkVerificationWarehouse,
    VerificationWarehouse,
)
from soda.contracts.impl.logs import Logs
from soda.contracts.impl.soda_cloud import SodaCloud
from soda.contracts.impl.yaml_helper import YamlFile


class ContractVerificationBuilder:

    def __init__(self):
        self.logs: Logs = Logs()
        self.warehouse_yaml_files: list[YamlFile] = []
        self.warehouse_spark_sessions: dict[str, object] = {}
        self.contract_files: list[YamlFile] = []
        self.soda_cloud_files: list[YamlFile] = []
        self.variables: dict[str, str] = {}

    def with_contract_yaml_file(self, contract_yaml_file_path: str) -> ContractVerificationBuilder:
        if not isinstance(contract_yaml_file_path, str):
            self.logs.error(
                message=f"In ContractVerificationBuilder, parameter contract_yaml_file_path must be a string, but was {contract_yaml_file_path} ({type(contract_yaml_file_path)})"
            )
        self.contract_files.append(YamlFile(yaml_file_path=contract_yaml_file_path, logs=self.logs))
        return self

    def with_contract_yaml_str(self, contract_yaml_str: str) -> ContractVerificationBuilder:
        assert isinstance(contract_yaml_str, str)
        self.contract_files.append(YamlFile(yaml_str=contract_yaml_str, logs=self.logs))
        return self

    def with_contract_yaml_dict(self, contract_yaml_dict: dict) -> ContractVerificationBuilder:
        assert isinstance(contract_yaml_dict, dict)
        self.contract_files.append(YamlFile(yaml_dict=contract_yaml_dict, logs=self.logs))
        return self

    def with_warehouse_yaml_file(self, warehouses_yaml_file_path: str) -> ContractVerificationBuilder:
        assert isinstance(warehouses_yaml_file_path, str)
        warehouse_yaml_file = YamlFile(yaml_file_path=warehouses_yaml_file_path, logs=self.logs)
        self.warehouse_yaml_files.append(warehouse_yaml_file)
        return self

    def with_warehouse_yaml_str(self, warehouses_yaml_str: str) -> ContractVerificationBuilder:
        assert isinstance(warehouses_yaml_str, str)
        warehouse_yaml_file = YamlFile(logs=self.logs, yaml_str=warehouses_yaml_str)
        self.warehouse_yaml_files.append(warehouse_yaml_file)
        return self

    def with_warehouse_yaml_dict(self, warehouses_yaml_dict: dict) -> ContractVerificationBuilder:
        assert isinstance(warehouses_yaml_dict, dict)
        warehouse_yaml_file = YamlFile(logs=self.logs, yaml_dict=warehouses_yaml_dict)
        self.warehouse_yaml_files.append(warehouse_yaml_file)
        return self

    def with_warehouse_spark_session(
        self, spark_session: object, warehouse_name: str = "spark_ds"
    ) -> ContractVerificationBuilder:
        assert isinstance(spark_session, object) and isinstance(warehouse_name, str)
        self.warehouse_spark_sessions[warehouse_name] = spark_session
        return self

    def with_variable(self, key: str, value: str) -> ContractVerificationBuilder:
        self.variables[key] = value
        return self

    def with_variables(self, variables: dict[str, str]) -> ContractVerificationBuilder:
        if isinstance(variables, dict):
            self.variables.update(variables)
        return self

    def with_soda_cloud_yaml_file(self, soda_cloud_yaml_file_path: str) -> ContractVerificationBuilder:
        assert isinstance(soda_cloud_yaml_file_path, str)
        self.soda_cloud_files.append(YamlFile(yaml_file_path=soda_cloud_yaml_file_path, logs=self.logs))
        return self

    def with_soda_cloud_yaml_str(self, soda_cloud_yaml_str: str) -> ContractVerificationBuilder:
        assert isinstance(soda_cloud_yaml_str, str)
        self.soda_cloud_files.append(YamlFile(yaml_str=soda_cloud_yaml_str, logs=self.logs))
        return self

    def with_soda_cloud_yaml_dict(self, soda_cloud_yaml_dict: dict) -> ContractVerificationBuilder:
        assert isinstance(soda_cloud_yaml_dict, dict)
        self.soda_cloud_files.append(YamlFile(yaml_dict=soda_cloud_yaml_dict, logs=self.logs))
        return self

    def build(self) -> ContractVerification:
        return ContractVerification(contract_verification_builder=self)

    def execute(self) -> ContractVerificationResult:
        contract_verification: ContractVerification = self.build()
        return contract_verification.execute()


class VerificationWarehouses:
    def __init__(self, contract_verification_builder: ContractVerificationBuilder):
        self.verification_warehouses_by_name: dict[str, VerificationWarehouse] = {}
        # The purpose of the undefined verification warehouse is to ensure that we still capture
        # all the parsing errors in the logs, even if there is no warehouse associated
        self.undefined_verification_warehouse = VerificationWarehouse()
        self.single_verification_warehouse: VerificationWarehouse | None = None
        self.logs: Logs = contract_verification_builder.logs

        # Parse data sources
        variables: dict[str, str] = contract_verification_builder.variables
        for warehouse_yaml_file in contract_verification_builder.warehouse_yaml_files:
            warehouse_yaml_file.parse(variables)
            verification_warehouse: VerificationWarehouse = FileVerificationWarehouse(
                warehouse_yaml_file=warehouse_yaml_file
            )
            self.add(verification_warehouse)
        for warehouse_name, spark_session in contract_verification_builder.warehouse_spark_sessions.items():
            verification_warehouse: VerificationWarehouse = SparkVerificationWarehouse(
                spark_session=spark_session, warehouse_name=warehouse_name
            )
            self.add(verification_warehouse)

    def get(self, contract_warehouse_name: str | None) -> VerificationWarehouse:
        if isinstance(contract_warehouse_name, str):
            verification_warehouse = self.verification_warehouses_by_name.get(contract_warehouse_name)
            if verification_warehouse:
                return verification_warehouse
            else:
                self.logs.error(f"Data source '{contract_warehouse_name}' not configured")
                return self.undefined_verification_warehouse

        if self.single_verification_warehouse:
            # no data source specified in the contract
            # and a single data source was specified in the verification
            return self.single_verification_warehouse

        return self.undefined_verification_warehouse

    def add(self, verification_warehouse: VerificationWarehouse):
        self.verification_warehouses_by_name[verification_warehouse.warehouse.warehouse_name] = verification_warehouse
        # update self.single_verification_warehouse because the number of verification warehouses changed
        warehouses_count = len(self.verification_warehouses_by_name)
        if warehouses_count == 1:
            self.single_verification_warehouse = next(iter(self.verification_warehouses_by_name.values()))
        elif warehouses_count == 0:
            self.single_verification_warehouse = self.undefined_verification_warehouse

    def __iter__(self) -> Iterator[VerificationWarehouse]:
        return iter(self.verification_warehouses_by_name.values())


class ContractVerification:

    @classmethod
    def builder(cls) -> ContractVerificationBuilder:
        return ContractVerificationBuilder()

    def __init__(self, contract_verification_builder: ContractVerificationBuilder):
        self.logs: Logs = contract_verification_builder.logs
        self.variables: dict[str, str] = contract_verification_builder.variables
        self.contracts: list[Contract] = []
        self.contract_results: list[ContractResult] = []
        self.soda_cloud: SodaCloud | None = None
        self.verification_warehouses = self._parse_verification_warehouses(contract_verification_builder)

        # parse the contract files and add them to the matching verification data source
        for contract_file in contract_verification_builder.contract_files:
            contract_file.parse(self.variables)
            if contract_file.is_ok():
                contract_warehouse_name: str | None = contract_file.dict.get("warehouse")

                verification_warehouse = self.verification_warehouses.get(contract_warehouse_name)

                contract: Contract = Contract.create(
                    warehouse=verification_warehouse.warehouse,
                    contract_file=contract_file,
                    variables=self.variables,
                    soda_cloud=self.soda_cloud,
                    logs=contract_file.logs,
                )
                verification_warehouse.add_contract(contract)
                self.contracts.append(contract)

        for soda_cloud_file in contract_verification_builder.soda_cloud_files:
            if soda_cloud_file.exists():
                soda_cloud_file.parse(self.variables)
                self.soda_cloud = SodaCloud(soda_cloud_file)
                break

    def _parse_verification_warehouses(self, contract_verification_builder) -> VerificationWarehouses:
        return VerificationWarehouses(contract_verification_builder)

    def __str__(self) -> str:
        return str(self.logs)

    def execute(self) -> ContractVerificationResult:
        all_contract_results: list[ContractResult] = []
        for verification_warehouse in self.verification_warehouses:
            warehouse_contract_results: list[ContractResult] = verification_warehouse.ensure_open_and_verify_contracts()
            all_contract_results.extend(warehouse_contract_results)
        return ContractVerificationResult(
            logs=self.logs, variables=self.variables, contract_results=all_contract_results
        )


class ContractVerificationResult:
    def __init__(self, logs: Logs, variables: dict[str, str], contract_results: list[ContractResult]):
        self.logs: Logs = logs
        self.variables: dict[str, str] = variables
        self.contract_results: list[ContractResult] = contract_results

    def failed(self) -> bool:
        """
        Returns True if there are execution errors or if there are check failures.
        """
        return not self.passed()

    def passed(self) -> bool:
        """
        Returns True if there are no execution errors and no check failures.
        """
        return not self.logs.has_errors() and all(contract_result.passed() for contract_result in self.contract_results)

    def has_errors(self) -> bool:
        return self.logs.has_errors()

    def has_failures(self) -> bool:
        return any(contract_result.failed() for contract_result in self.contract_results)

    def is_ok(self) -> bool:
        return not self.has_errors() and not self.has_failures()

    def assert_ok(self) -> ContractVerificationResult:
        errors_str: str | None = self.logs.get_errors_str() if self.logs.get_errors() else None
        if errors_str or any(contract_result.failed() for contract_result in self.contract_results):
            raise SodaException(message=errors_str, contract_verification_result=self)
        return self

    def __str__(self) -> str:
        blocks: list[str] = [str(self.logs)]
        for contract_result in self.contract_results:
            blocks.extend(self.__format_contract_results_with_heading(contract_result))
        return "\n".join(blocks)

    @classmethod
    def __format_contract_results_with_heading(cls, contract_result: ContractResult) -> list[str]:
        return [f"# Contract results for {contract_result.contract.dataset}", str(contract_result)]


class SodaException(Exception):
    """
    See also adr/03_exceptions_vs_error_logs.md
    """

    def __init__(
        self, message: str | None = None, contract_verification_result: ContractVerificationResult | None = None
    ):
        self.contract_verification_result: ContractVerificationResult | None = contract_verification_result
        message_parts: list[str] = []
        if message:
            message_parts.append(message)
        if self.contract_verification_result:
            message_parts.append(str(self.contract_verification_result))
        exception_message: str = "\n".join(message_parts)
        super().__init__(exception_message)
