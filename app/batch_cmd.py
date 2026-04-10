import pandas as pd
import logging
from engine.device_operator import DeviceOperator

logger = logging.getLogger(__name__)

class BatchCmdRunner:
    """
    Orchestrates batch execution of commands from Excel/CSV.
    Handles variable substitution and high-level flow control.
    """
    def __init__(self, operator: DeviceOperator):
        self.operator = operator
        self.variables = {}
        self.summary = []

    def run_file(self, file_path: str):
        """Reads the command list and iterates through each step."""
        df = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
        
        for _, row in df.iterrows():
            # Resolve ${var} placeholders in the command content
            content = self._resolve_placeholders(str(row['Content']))
            
            # Delegate pure device operation to the Operator
            result = self.operator.execute_and_verify(
                task_type=row['Type'],
                content=content,
                expect=row.get('Expect'),
                **row.to_dict()
            )
            
            # Register output as a variable if requested
            reg_name = row.get('Register')
            if pd.notna(reg_name) and result['status'] == "PASS":
                self.variables[str(reg_name)] = str(result['actual'])
            
            self.summary.append({"name": row['Name'], "status": result['status']})
            logger.info(f"Step '{row['Name']}': {result['status']}")

    def _resolve_placeholders(self, text: str) -> str:
        """Standard variable replacement logic."""
        for var_name, value in self.variables.items():
            text = text.replace(f"${{{var_name}}}", value)
        return text