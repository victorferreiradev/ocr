# Importa as bibliotecas necessárias
from flask import Flask, render_template, request  # Importa o Flask e funções relacionadas para renderizar templates e lidar com requisições
from PIL import Image  # Importa o módulo Image da biblioteca Pillow para manipulação de imagens
import pytesseract  # Importa pytesseract para realizar OCR (Reconhecimento Óptico de Caracteres) em imagens
import re  # Importa o módulo re para expressões regulares

# Define o caminho para o executável do Tesseract, necessário se o caminho não estiver no PATH do sistema
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
print("Caminho do Tesseract:", pytesseract.pytesseract.tesseract_cmd)


# Cria uma instância do aplicativo Flask
app = Flask(__name__)

def preprocess_image(image):
    """
    Função para pré-processar a imagem para melhorar a precisão do OCR.
    """
    gray_image = image.convert('L')  # Converte a imagem para escala de cinza (L)
    enhanced_image = gray_image.point(lambda x: 0 if x < 128 else 255)  # Aplica um filtro de binarização: define pixels abaixo de 128 como preto e acima como branco
    return enhanced_image  # Retorna a imagem processada

def sum_numbers_from_image(image):
    """
    Função para extrair números da imagem e calcular a soma.
    """
    img = preprocess_image(image)  # Pré-processa a imagem
    text = pytesseract.image_to_string(img, config='--psm 6')  # Extrai o texto da imagem usando pytesseract com o modo de layout de página 6 (suporta textos em bloco)
    print("Texto extraído:", text)  # Imprime o texto extraído para depuração
    
    numbers = re.findall(r'\d+(?:\.\d+)*', text)  # Encontra todos os números no texto extraído usando expressões regulares

    cleaned_numbers = [num.replace('.', '') for num in numbers]  # Remove os pontos decimais dos números (para lidar com formatação inconsistente)
    
    numbers = [float(num) for num in cleaned_numbers]  # Converte os números limpos para floats
    
    total_sum = sum(numbers)  # Calcula a soma total dos números
    
    return total_sum  # Retorna a soma total

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    """
    Função para lidar com uploads de imagem e exibir o resultado da soma.
    """
    total_sum = None

    if request.method == 'POST':  # Verifica se o método da requisição é POST (upload de imagem)
        file = request.files['image']  # Obtém o arquivo enviado no formulário
        if file:  # Verifica se um arquivo foi enviado
            img = Image.open(file)  # Abre a imagem usando Pillow
            total_sum = sum_numbers_from_image(img)  # Calcula a soma dos números extraídos da imagem
            return f'A soma dos valores na imagem é: {total_sum:.3f}'  # Retorna o resultado formatado como texto
    return render_template('index.html')  # Renderiza a página inicial se o método da requisição não for POST

if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask em modo de depuração
