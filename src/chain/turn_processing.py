from src.chain.processing import processing
from src.models.storage_row_turn_model import storage_row_turn_model

class turn_processing(processing):
    
    def process(self, source: list) -> list:
        super().process(source)
        result = []
        
        grouped_transactions = {}
        for transaction in source:
            key = f"{transaction.nomenclature.unique_code}_{transaction.storage.unique_code}_{transaction.unit.unique_code}"
            if key not in grouped_transactions.keys():
                grouped_transactions[key] = []
                
            grouped_transactions[key].append(transaction)

        for key, transactions in grouped_transactions.items():
            first_transaction = transactions[0]
            
            turnover = sum(transaction.value if transaction.storage_type else -transaction.value for transaction in transactions)
               
            row = storage_row_turn_model.create( first_transaction.nomenclature, first_transaction.storage, first_transaction.unit)
            row.value = turnover
            
            result.append(row)

        return result
 
  