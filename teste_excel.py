from src.services.excel_service import ExcelService

service = ExcelService()

perguntas = service.carregar("data/quiz.xlsx")

print(f"Foram carregadas {len(perguntas)} perguntas.\n")

for pergunta in perguntas:
    print(pergunta.texto)
