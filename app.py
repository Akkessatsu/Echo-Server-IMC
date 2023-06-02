class App():
    def __init__(self):
        """Generates a title and a header for information at 
        the instance of the class.
        """
        
        App.title("The shape of us!")
        print()
        print("=> Informe alguns dados para começar: ")
        print()
        App.generate_header()

    @classmethod
    def padding(cls):
        """Generates two linebreaks
        """
        print()
        print()

    @classmethod
    def generate_header(cls):
        """Generates a header that indicates some information about
        level of activity.
        """
        print("OBS: O Nivel de atividade varia de 1 (Sedentário) a 4 (Muito Ativo) !")
        print(f"Ex: {'1.70':^8s} {'70.0':^22s} {'M':^14s} {'3':^20s} {'20':^10s} ")
        print()

    @classmethod
        
    def row(cls):
        """Generates a row of 81 asterisks.
        """
        print('*' * 81)

    @classmethod
    def row_table(cls):
        """Generates a table row in the following format:
        '+-------------------------++-------------------------++-------------------------+'
        """
        print(f"+{'-' * 25}++{'-' * 25}++{'-' * 25}+")

    @classmethod
    def title(cls, title: str):
        """Generates a formatted title.

        Args:
            title: A string containing the title to be formatted.
        """
        App.row()
        print(f'*{title:^79s}*')
        App.row()

    @classmethod
    def collect_user_data(cls) -> list:
        """Collect user information and returns it

        Returns:
            Returns a list containing the user data passed 
            to the function (Height, Mass, Sex, Lvl of Activity, Age)
        """
        print(f"{'Altura (m):':^16s}", end="")
        print(f"{'Peso (Kg):':^18s}", end="")
        print(f"{'Sexo (M/F):':^18s}", end="")
        print(f"{'Nvl de Ativ:':^18s}", end="")
        print(f"{'Idade :':^16s}")

        user_data = input("")
        user_data = user_data.split(" ")
        print()
        App.row()

        return user_data

    @classmethod
    def list_user_data(cls, values: list[str]) -> list[str|float]:
        """Returns the user data as a list with its elements converted.

        Args:
            values: 
                The collected user data obtained by collect_user_data
                function.

        Returns:
            A list containing the elements of collect_user_data as a float
            if it is not a empty value or a string value.
        """
        list = []
        for i in values:
            if i != "":
                if (i in "Mm" or i in "Ff"):
                    list.append(i)
                else:
                    list.append(float(i))
        return list

    @classmethod
    def generate_dict(cls, list: list[str|float]) -> dict[str:float|str]:
        """Generates a dictionary given a list of values.
        
        Args
            list: 
                The collected user data obtained as a list of string and float elements
        Returns:
            Generates a dictionary based on the list of user data passed as argument.
        """
        user_information = [
                'altura',
                'peso',
                'sexo',
                'nvlAtiv',
                'idade'
               ]
        dic = {
            elm: list[cont] for cont, elm in enumerate(user_information)
        }
        return dic

    @classmethod
    def validate_data(cls, values:list[str]) -> list[str|float]:
        """Returns the collected user data if it is valid.
        
        Args:
            values: A list of strings obtained by the collect_user_data function.

        Returns:
            Returns the result of the list_user_data function
            if all fields of the data are collected and there are not any data type mismatch
            between the input of the user and the required data.
        """
        while True:
            try:
                list = App.list_user_data(values)
                user_data = App.generate_dict(list)

            except IndexError:
                print()
                print('Preencha todos os dados para prosseguir!'.upper())
                print()
                App.generate_header()
                values = App.collect_user_data()

            except ValueError:
                print()
                print('Valor inválido!'.upper())
                print()
                App.generate_header()
                values = App.collect_user_data()

            else:
                list = App.list_user_data(values)
                break

        return list

    @classmethod
    def print_result(cls, list: list[str]):
        """Generates a printed message containing the result
        of TMB, IMC o QtdCal

        Args:
            list (list[str]): The result of user TMB, BMI or QtdCal
        """
        print()
        App.row()
        print(f"|{str(list[0][0]):^25s}||{str(list[0][1]):^25s}||{str(list[0][2]):^25s}|")
        App.row()

    @classmethod
    # (imc, status)
    def create_table_imc(cls, imc: float, status: str):
        """Generates a table containing information about BMI and the user BMI

        Args:
            imc: The value of the user BMI
            status: A message that indicates in which status the user fits
        """
        content = [['Tabela de IMC', 'Intervalo', ' Status'],
                   ['Menos do que: ', '18,5', 'Abaixo do Peso !'],
                   ['Entre: ', '18,5 e 24,9', 'Peso Normal!'],
                   ['Entre: ', '25,0 e 29,9', 'Sobrepeso!'],
                   ['Entre: ', '30,0 e 34,9', 'Obesidade Grau 1!'],
                   ['Entre: ', '35,0 e 39,9', 'Obesidade Grau 2!'],
                   ['Mais do que: ', '40,0', 'Obesidade Grau 3!'],
                   ]

        # analysingImc -> status
        result = [['SEU IMC: ', str(imc), status]]
        print()
        
        for row in range(0, len(content)):
            App.row_table()
            print(f"|{content[row][0]:^25s}||{content[row][1]:^25s}||{content[row][2]:^25s}|")
            
            if row == 6:
                App.row_table()
                App.print_result(result)

    @classmethod
    def create_table_qtd_cal(cls, dict: dict[str:float|str]):
        """Generates a table containing information about quantity of calories

        Args:
            dict: 
                A dictionary that contains the names of nutrients as a key (carbohydrates, proteins, fats)
                and the amount of calories in each one as values.
                See generate_nutrients at server.py for more information about it
        """
        carboidratos_value = round(float((dict["carboidratos"])) / 4.0)
        proteinas_value    = round(float((dict["proteinas"])) / 4.0)
        gorduras_value     = round(float((dict["gorduras"])) / 9.0)
        
        content = [
            ["Carboidratos: ", dict["carboidratos"], carboidratos_value, 2],
            ["Proteínas: ",    dict["proteinas"],    proteinas_value, 2],
            ["Gorduras",       dict["gorduras"],     gorduras_value, 2]
        ]

        for row in range(0, len(content)):
            App.row_table()
            print('|{:^25}||{:^25}||{:^25}|'.format(str(content[row][0]),
                                                    str(content[row][1]) + " kcal",
                                                    str(content[row][2]) + " g"))
            App.row_table()

    @classmethod
    def menu(cls, response: dict[str: float|dict[str: float]|str]):
        """Generates the main menu of the application

        Args:
            response: 
                A dictionary that contains all the user information('altura',
                'peso',
                'sexo',
                'nvlAtiv',
                'idade',
                'imc',
                'statusImc',
                'tmb',
                'calorias',
                'nutrientes'
                )
                collected and generated by the functions of the application.
        """
        while True:
            App.padding()
            print("=> Selecione uma opção: ")
            print()
            print(f'{"1 - IMC":^16s}{"2 - TMB":^18s}{"3 -  QTD KCAL":^18s}{"4 - SAIR":^18s}{"":2s}', end="\t")
            opt = input()
            App.padding()

            match opt:
                case '1':
                    App.title("IMC")
                    print()
                    print("{:^81s}".format(
                        "O Indice de Massa Corporal (IMC) é um parâmetro"))
                    
                    print("{:^81s}".format(
                        "utilizado para saber se o peso está de acordo com a altura de um"))
                    
                    print("{:^81s}".format(
                        "indivíduo, o que pode interferir diretamente na sua saúde e qualidade de vida!"))
                    
                    App.create_table_imc(response["imc"], response["statusImc"])
                    
                case '2':
                    App.title("Taxa Metabólica Basal: ")
                    print()
                    print("{:^81s}".format(
                        "A Taxa de Metabolismo Basal (TMB) é a quantidade"))
                    
                    print("{:^81s}".format(
                        "mínima de energia (calorias) necessária para manter as"))
                    
                    print("{:^81s}".format(
                        "funções vitais do organismo em repouso. Essa taxa pode variar"))
                    
                    print("{:^81s}".format(
                        "de acordo com o sexo, peso, altura, idade e nível de atividade física."))

                    result = [['RESULTADO :', 'SUA TMB:', str(response['tmb']) + " kcal"]]
                    App.print_result(result)
                    
                case '3':
                    nut = response["nutrientes"]
                    App.title("Quantidade de Calorias: ")
                    print()
                    print("{:^81s}".format(
                        "Calorias são a quantidade de energia que um determinado alimento"))
                    
                    print("{:^81s}".format(
                        "fornece após ser consumido, contribuindo para as funções essenciais do"))
                    
                    print("{:^81s}".format(
                        "organismo, como respiração, produção de hormônios, e funcionamento do cérebro."))

                    print()
                    print("{:^81s}".format(
                        "Você deve consumir aproximadamente: "))
                    print()
                    App.create_table_qtd_cal(nut)

                    result = [['RESULTADO :', 'SUA QTD DE KCAL:', str(response['cal']) + " kcal"]]
                    App.print_result(result)
                    
                case '4':
                    print('{:^79s}'.format("Obrigado por usar nosso App !"))
                    App.padding()
                    App.row()
                    break
                
                case _:
                    print("Erro: Opção Inválida!")