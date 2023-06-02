# server.py
import socket
import json

# create a socket object
print('ECHO SERVER para cálculo do IMC')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get a local machine name
host = '127.0.0.1'
port = 9999

# bind to the port
server_socket.bind((host, port))

#start listening requests
server_socket.listen()
print(f'Serviço rodando na porta {port}.')

while True:
    # establish a connection
    client_socket, addr = server_socket.accept()
    print(f'Conectado a {str(addr)}')

    # receive client data
    received = client_socket.recv(1024).decode()

    print(f'Os dados recebidos do cliente são: {received}')

    # server processing
    received = json.loads(received)

    # IMC (Indice de Massa Corporal)
    def generate_imc(dict: dict[str:float|str]) -> float:
        """Computes and returns the user BMI.

        Args:
            dict: A dictionary that contains the user data collected and passed
            by the functions: validate_data and generate_dict. 

        Returns:
            A float value that represents the user BMI.
        """
        h = dict['altura']
        p = dict['peso']
        return round(float(p / (h * h)), 2)

    # adding the imc to data sent by the user
    received['imc'] = generate_imc(received)

    # Status IMC
    def analyse_imc(imc: float) -> str:
        """Returns a message based in the argument.

        Args:
            imc: A value that represents the user BMI.
        """
        if imc > 0 and imc < 18.5:
            status = "Abaixo do Peso!"
        elif imc <= 24.9:
            status = "Peso normal!"
        elif imc <= 29.9:
            status = "Sobrepeso!"
        elif imc <= 34.9:
            status = "Obesidade Grau 1!"
        elif imc <= 39.9:
            status = "Obesidade Grau 2!"
        elif imc <= 40.0:
            status = "Obesidade Grau 1!"
        else:
            status = "Valores inválidos"
        return status

    # adding the status of the imc to data sent by the user
    received['statusImc'] = analyse_imc(received['imc'])

    # TMB (Taxa Metabólica Basal)
    def generate_TMB(dict: dict[str:float|str]) -> float:
        """Computes and returns the user TMB.

        Args:
            dict: A dictionary that contains the user data collected and passed
            by the functions: validate_data and generate_dict. 

        Returns:
            A float value that represents the user TMB.
        """
        sex = dict['sexo']

        if sex in 'Mm':
            tmb = 5 + (10 * dict['peso']) + (6.25 * (dict['altura'] * 100)) - (5 * dict['idade'])
        else:
            tmb = (10 * dict['peso']) + (6.25 * (dict['altura'] * 100)) - (5 * dict['idade']) - 5

        return tmb

    # adding the tmb to data sent by the user
    received['tmb'] = generate_TMB(received)

    def generate_cal(dict: dict[str:float|str]) -> float:
        """Computes and returns the user quantity of calories.

        Args:
            dict: A dictionary that contains the user data collected and passed
            by the functions: validate_data and generate_dict. 

        Returns:
            A float value that represents the user quantity of calories.
        """
        match dict['nvl_ativ']:
            case 1:
                fator_ativ = 1.2
            case 2:
                fator_ativ = 1.375
            case 3:
                fator_ativ = 1.725
            case _:
                fator_ativ = 1.9

        return round((dict['tmb'] * fator_ativ), 2)

    # adding the cal to data sent by the user
    received['cal'] = generate_cal(received)

    def generate_nutrients(dict: dict[str:float|str]) -> dict[str: float]:
        """Computes and returns the user quantity of nutrients.

        Args:
            dict: A dictionary that contains the user data collected and passed
            by the functions: validate_data and generate_dict. 

        Returns:
            A dictionary that represents the user quantity of nutrientes.
            The key is the name of the nutrient and the value its quantity
            of calories.
        """
        carb_value = (dict['cal'] * 0.45)
        prot_value = (dict['cal'] * 0.3)
        fat_value  = (dict['cal'] * 0.25)
        
        carb = str(round(carb_value, 2))
        prot = str(round(prot_value, 2))
        fat =  str(round(fat_value, 2))

        return {"carboidratos": carb, "proteinas": prot, "gorduras": fat}

    # adding the nutrients to data sent by the user
    received["nutrientes"] = generate_nutrients(received)
    print(f'O resultado do processamento é {received}')

    # serialising
    result = json.dumps(received)

    # send a result
    client_socket.send(result.encode('ascii'))
    print('Os dados do cliente foram enviados com sucesso!')

    # finish a connection
    client_socket.close()