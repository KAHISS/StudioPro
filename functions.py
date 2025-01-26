# interface libs =================================
from largeVariables import *
from tkinter import messagebox
from customtkinter import *
from tkinter import filedialog
from tkinter import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import timedelta
# functions libs ==================================
import os
import requests
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from barcode import EAN13
from cv2_collage import create_collage
import shutil
import cairosvg


class GeneralFunctions:

    @staticmethod
    def backup_dataBase_local():
        # pick directory if origin =========================
        origin = './resources'
        destiny = os.path.join(os.path.expanduser("~"), "StudioPro/backup/resources")
        # coping ================================
        if os.path.exists(destiny):
            shutil.rmtree(destiny)
            shutil.copytree(origin, destiny)
        else:
            shutil.copytree(origin, destiny)

    def backup_dataBase_cloud(self):
        try:
            # making request in the site ========================
            request = requests.get("https://www.google.com/intl/pt-br/drive/about.html")
        except Exception:
            # error in request ===================
            self.message_window(typem=2, titlein='Backup local', messagein='Foi feito só o backup local, conecte-se a internet para fazer o backup na nuvem')
        else:
            # pick directory if origin =========================
            diretoryCloud = self.dataBases['backup'].searchDatabase("SELECT caminho FROM Load")[0][0]
            origin = './resources'
            destiny = os.path.join(diretoryCloud, "StudioPro/backup/resources")
            # coping ================================
            if os.path.exists(destiny):
                shutil.rmtree(destiny)
                shutil.copytree(origin, destiny)
            else:
                shutil.copytree(origin, destiny)

    def calculateDate(self, data_entrys, type_calculate='days'):
        initDate = datetime.strptime(data_entrys[0], "%d/%m/%Y")
        lastDate = datetime.strptime(data_entrys[1], "%d/%m/%Y")

        # pick the diference of days
        diferenceOfDays = (lastDate - initDate).days + 1

        informationsOfDays = []
        # trating values
        for quantityDays in range(diferenceOfDays):
            date = initDate + timedelta(days=quantityDays)

            match type_calculate:
                case 'payment':
                    # searching information of schedule =========================
                    informationsSchedule = self.dataBases['schedule'].searchDatabase(f'SELECT * FROM Agenda WHERE data LIKE "%{date.strftime("%d/%m/%Y")}%" AND profissional LIKE "%{data_entrys[2]}%" AND método_de_pagamento LIKE "%{data_entrys[3]}%"')
                    if informationsSchedule:
                        informationsOfDays.extend(informationsSchedule)
                case 'days':
                    # informations of schedule and sold ===========================================
                    informationsDay = self.dataBases['cash'].searchDatabase(f'SELECT * FROM Gerenciamento_do_dia WHERE data LIKE "%{date.strftime("%d/%m/%Y")}%" AND status LIKE "%DIA FINALIZADO%"')
                    if informationsDay:
                        informationsOfDays.append(informationsDay[0])

        # calculing values
        informationsOfInterval = [
            len([value for value in informationsOfDays if value[5] not in ['NÃO FOI PAGO', 'SEM PAGAMENTO', '']]),
            self.treating_numbers(
                type_treating=4,
                values=[value[3] for value in informationsOfDays if value[5] not in ['NÃO FOI PAGO', 'SEM PAGAMENTO', '']],
            ),
        ] if type_calculate == 'payment' else [
            self.treating_numbers(
                type_treating=6,
                values=[value[1] for value in informationsOfDays],
            ),
            self.treating_numbers(
                type_treating=6,
                values=[value[2] for value in informationsOfDays]
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=3
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=4
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=5
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=6
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=7
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=8
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=9
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=10
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=11
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=12
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=13
            ),
            self.treating_numbers(
                type_treating=2,
                values=informationsOfDays,
                ide=14
            ),
        ]
        return informationsOfInterval

    def loading_database_local(self):
        doLoad = self.dataBases['backup'].searchDatabase('SELECT * FROM Load')[0][0]
        if doLoad == 'sim':
            # pick directory if origin =========================
            origin = os.path.join(os.path.expanduser("~"), "StudioPro/backup/resources")
            destiny = './resources'
            # coping ================================
            if os.path.exists(origin):
                shutil.rmtree(destiny)
                shutil.copytree(origin, destiny)

    def loading_database_cloud(self):
        try:
            # making request in the site ========================
            request = requests.get("https://www.google.com/intl/pt-br/drive/about.html")
        except Exception:
            # error in request ===================
            self.loading_database_local()
            self.message_window(typem=2, titlein='Backup local', messagein='Foi carregado o backup local, conecte-se a internet para fazer o sincronização com a nuvem')
        else:
            # pick directory if origin =========================
            diretoryCloud = self.dataBases['backup'].searchDatabase("SELECT caminho FROM Load")[0][0]
            origin = os.path.join(diretoryCloud, "StudioPro/backup/resources")
            destiny = './resources'
            # coping ================================
            if os.path.exists(origin):
                shutil.rmtree(destiny)
                shutil.copytree(origin, destiny)

    def insert_treeview_informations(self, treeview, infos, line_color):
        for info in infos:
            if self.lineTreeviewColor[line_color] % 2 == 0:
                treeview.insert('', 'end', values=info, tags='oddrow')
            else:
                treeview.insert('', 'end', values=info, tags='evenrow')
            self.lineTreeviewColor[line_color] += 1

    def select_diretory_of_cloud(self):
        # select diretory ==========================
        diretory = filedialog.askdirectory(title='Escolha o diretório da nuvem')
        # updating backup
        self.dataBases['backup'].crud(f'UPDATE Load SET caminho = "{diretory}"')

    @staticmethod
    def pick_informations_treeview(treeview):
        selection = treeview.get_children()
        information = []
        for i in selection:
            information.append(treeview.item(i, 'values'))
        return information

    @staticmethod
    def selection_treeview(treeview):
        selection = treeview.selection()
        information = []
        for i in selection:
            information.append(treeview.item(i, 'values'))
        return information

    @staticmethod
    def validation(infos, type_validation, index=None):
        if type_validation == 1:
            for info in infos[0]:
                if info == '' or info == 'R$,00':
                    return False
        elif type_validation == 2:
            if not infos.replace('.', '', 1).isdigit():
                return False
        elif type_validation == 3:
            for c in infos:
                if c.isalpha() or c == '.':
                    return False
        elif type_validation == 4:
            for c in infos[2:]:
                if c.isalpha() or c == '.':
                    return False
        elif type_validation == 5:
            for info in infos:
                if info == '' or info == 'R$,00' or info == ':00':
                    return False
        elif type_validation == 6:
            for c in infos:
                if c.isalpha() or c == '.':
                    return False
            if len(infos) != 12:
                return False
        elif type_validation == 7:
            for info in infos:
                for c in info:
                    if c.isalpha() or c == '.':
                        return False
        elif type_validation == 8:
            for info in infos:
                for c in info[2:]:
                    if c.isalpha() or c == '.':
                        return False
        return True

    @staticmethod
    def treating_numbers(info=None, type_treating=1, values=None, entry2=None, ide=3):
        if type_treating == 1:
            if ',' in info:
                value = info.replace('R$', '').strip().split(',')
                if value[1] == '':
                    return 'R$' + ','.join(value) + '00'
                else:
                    return 'R$' + ','.join(value)
            else:
                value = info.replace('R$', '').strip()
                return 'R$' + value + ',00'

        elif type_treating == 2:
            sum_value = 0
            for value in values:
                number = float(value[ide].replace('R$', '').replace(',', '.'))
                sum_value += number
            return 'R$' + f'{sum_value:.2f}'.replace('.', ',')

        elif type_treating == 3:
            if ':' in info:
                hour = info.split(':')
                if hour[1] == '':
                    hour[1] = '00'
                if hour[0] == '':
                    hour[0] = '00'
                if len(hour[0]) == 1:
                    hour[0] = '0' + hour[0]
                if hour[0] and hour[1] == '':
                    hour[0], hour[1] = '00'
                return ':'.join(hour)
            else:
                if len(info) == 1:
                    info = '0' + info
                return info + ':00'

        elif type_treating == 4:
            sum_value = 0
            for value in values:
                number = float(value.replace('R$', '').replace(',', '.'))
                sum_value += number
            return 'R$' + f'{sum_value:.2f}'.replace('.', ',')

        elif type_treating == 5:
            subtraction_value = float(values[0].replace('R$', '').replace(',', '.'))
            for value in values[1:]:
                number = float(value.replace('R$', '').replace(',', '.'))
                subtraction_value -= number
            return 'R$' + f'{subtraction_value:.2f}'.replace('.', ',')

        elif type_treating == 6:
            sum_value = 0
            for value in values:
                number = float(value.replace('R$', '').replace(',', '.'))
                sum_value += number
            return int(sum_value)

        elif type_treating == 7:
            number = float(info.replace('R$', '').replace(',', '.'))
            return number

        elif type_treating == 8:
            phone = info.get().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            phoneFormated = ''
            if len(info.get()) == 9:
                phoneFormated = f'(77) {phone[0:5]}-{phone[5:]}'
            if len(info.get()) >= 11:
                phoneFormated = f'({phone[0:2]}) {phone[2:7]}-{phone[7:]}'
            info.delete(0, END)
            info.insert(0, phoneFormated)

        elif type_treating == 9:
            cpf = info.get().replace(' ', '').replace('-', '').replace('.', '')
            cpfFormated = ''
            if len(info.get()) == 11:
                cpfFormated = f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
            else:
                cpfFormated = info.get()
            info.delete(0, END)
            info.insert(0, cpfFormated)

        elif type_treating == 10:
            sum_value = 0
            for value in values:
                number = float(value[ide].replace('R$', '').replace(',', '.'))
                sum_value += number
            return int(sum_value)

    def delete_informations_treeview(self, treeview, line_color):
        for linhas in treeview.get_children():
            treeview.delete(linhas)
        self.lineTreeviewColor[line_color] = 0

    def message_window(self, typem=1, titlein='', messagein=''):
        if typem == 1:
            messagebox.showinfo(title=titlein, message=messagein)
        elif typem == 2:
            messagebox.showwarning(title=titlein, message=messagein)
        elif typem == 3:
            messagebox.showerror(title=titlein, message=messagein)
        elif typem == 4:
            question = messagebox.askyesno(title=titlein, message=messagein)
            return question
        self.root.focus_force()

    def insert_informations_entrys(self, entrys, treeview=None, insert=True, type_insert='normal', table='', photo=None, size=(170, 200), data_base='informations'):
        match type_insert:
            case 'normal':
                # deleting informations of entrys ===============================
                for entry in entrys:
                    if isinstance(entry, CTkComboBox):
                        entry.set('')
                    elif isinstance(entry, CTkTextbox):
                        entry.delete('0.0', END)
                    else:
                        entry.delete(0, END)
                # cheking if there is information in the treeview ================================
                if insert:
                    if treeview.selection():
                        for index, information in enumerate(self.selection_treeview(treeview)[0][1:-1]):
                            if isinstance(entrys[index], CTkComboBox):
                                entrys[index].set(information)
                            elif isinstance(entrys[index], CTkTextbox):
                                entrys[index].insert('0.0', information)
                            else:
                                entrys[index].insert(0, information)
                                if entrys[index] == self.passwordEntry:
                                    entrys[index].delete(0, END)
            case 'advanced':
                # deleting informations of entrys ===============================
                for entry in entrys:
                    if isinstance(entry, CTkComboBox) or isinstance(entry, StringVar):
                        entry.set('')
                    elif isinstance(entry, CTkLabel):
                        self.pick_picture(entry, photo, 'unknow')
                    elif isinstance(entry, CTkTextbox):
                        entry.delete('0.0', END)
                    else:
                        entry.delete(0, END)
                if insert:
                    # cheking if there is information in the treeview ================================
                    if treeview.selection():
                        informations = self.selection_treeview(treeview)[0]
                        # case informations is of cash day
                        if 'R$' in informations[3]:
                            if treeview == self.treeviewCashDayGeneral:
                                informations = informations[0:9] + informations[14:17]
                            else:
                                informations = informations[0:9] + informations[14:17]
                        if treeview == self.treeviewCashPayment:
                            informations = informations[0:9]

                        for index, information in enumerate(informations[1:] if treeview not in [self.treeviewSaleInventoryControl, self.treeviewSaleInventoryControlUnusable] else informations[1:-1] + ('', '')):
                            if isinstance(entrys[index], CTkComboBox) or isinstance(entrys[index], StringVar):
                                entrys[index].set(information.capitalize() if isinstance(entrys[index], StringVar) else information)
                            elif isinstance(entrys[index], CTkLabel):
                                self.pick_picture(entrys[index], photo, 'toggle', self.dataBases[data_base].searchDatabase(f'SELECT foto FROM {table} WHERE ID = {informations[0]}')[0][0], size=size)
                            elif isinstance(entrys[index], CTkTextbox):
                                entrys[index].insert('0.0', self.dataBases[data_base].searchDatabase(f'SELECT observação FROM {table} WHERE ID = {informations[0]}')[0][0])
                            else:
                                entrys[index].insert(0, information)

    def delete_information(self, treeview, type_information, table):
        # pick up selection for delete information =============================
        if ask := self.message_window(4, 'Comfimação', 'Você tem certeza de que deseja deletar o(s) item(s) selecionado(s)'):
            for selection in self.selection_treeview(treeview):
                self.dataBases[type_information].crud(deleteInformation.format(table, selection[0]))
            if len(self.dataBases[type_information].searchDatabase(searchAll.format(table))) == 0:
                self.dataBases[type_information].crud(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
        return ask

    def insert_inputs_generalCash(self, treeview, entrys):
        for entry in entrys[0:11]:
            if isinstance(entry, CTkComboBox):
                entry.set('')
            else:
                entry.delete(0, END)

        informationsOfDays = self.selection_treeview(treeview)[0]

        # inserting informations of day ====================================
        for index, information in enumerate(informationsOfDays[1:8]):
            entrys[index].insert(0, information)
        entrys[7].insert(0, informationsOfDays[13])
        entrys[8].insert(0, informationsOfDays[14])
        entrys[9].insert(0, informationsOfDays[15][3:13])
        entrys[10].insert(0, informationsOfDays[15][18:])

    @staticmethod
    def create_pdf(treeview, elements):
        saveDirectory = filedialog.asksaveasfilename(defaultextension="*.pdf ", filetypes=[("Todos os Arquivos", "*.*"), ('Arquivos de pdf', "*.pdf")])
        if saveDirectory != '':
            # creating document ============================================
            document = SimpleDocTemplate(saveDirectory, pagesize=A4)
            # insert elements in document ==================================
            content = []
            for element in elements:
                content.append(element)
            document.build(elements)
            return saveDirectory

    @staticmethod
    def request_adrees(zip_code, informations):
        # treating the cep =============================
        treatedZipCode = zip_code.replace('-', '').replace(' ', '').replace('.', '')
        # validating if the zip code have eight numbers =======================
        if len(treatedZipCode) == 8:
            try:
                # making request in the site ========================
                request = requests.get(f'http://viacep.com.br/ws/{treatedZipCode}/json/').json()
            except Exception:
                # error in request ===================
                pass
            else:
                if len(request) > 1:
                    # deleting informations in the entrys =====================
                    for information in informations:
                        information.delete(0, END)
                    # insert informations in the entrys ========================
                    informations[0].insert(0, request['bairro'])
                    informations[1].insert(0, request['localidade'])
                    informations[2].insert(0, request['uf'])

    @staticmethod
    def image(file, size):
        try:
            if 'icon_no_picture.png' in file or 'icon_barCode.png' in file or 'icon_product.png' in file:
                size = (76, 76)
            img = CTkImage(light_image=Image.open(file), dark_image=Image.open(file), size=size)
        except FileNotFoundError:
            img = CTkImage(light_image=Image.open('assets/corrupted.png'), dark_image=Image.open('assets/corrupted.png'), size=(76, 76))
        return [img, file]

    def pick_picture(self, label, photo, type_photo='new', directory='', size=None):
        # pick directory of photo ======================================
        match type_photo:
            case 'new':
                fileName = filedialog.askopenfilename()
                if fileName:
                    self.photosAndIcons[photo] = self.image(fileName, (170, 200))
                    label.configure(image=self.photosAndIcons[photo][0])
            case 'toggle':
                self.photosAndIcons[photo] = self.image(directory, size)
                label.configure(image=self.photosAndIcons[photo][0])
            case 'unknow':
                if photo in ['employee', 'costumer']:
                    self.photosAndIcons[photo] = self.image(f'assets/icon_no_picture.png', (76, 76))
                elif photo == 'barCode':
                    self.photosAndIcons[photo] = self.image(f'assets/icon_barCode.png', (76, 76))
                elif photo in ['productUse', 'productSale', 'productUseUnusable', 'productSaleSold']:
                    self.photosAndIcons[photo] = self.image(f'assets/icon_product.png', (76, 76))
                label.configure(image=self.photosAndIcons[photo][0])

    @staticmethod
    def searching_list(first, quantity, column, insert=False, index=0, information=''):
        # create list of informations ===============================
        listSearch = [first]
        listSearch.extend([''] * quantity)
        listSearch.append(column)
        if insert:
            listSearch.insert(index, information)
        return listSearch

    def encode_for_searching(self, information):
        if information == '':
            return information
        else:
            return self.criptography.encode(information)

    def decode_informations_database(self, informations):
        # decoding informations ================================
        informationsDecode = []
        for information in informations:
            informationsDecode.append(
                (
                    information[0], self.criptography.decode(information[1][2:-1]), self.criptography.decode(information[2][2:-1]), self.criptography.decode(information[3][2:-1]),
                    self.criptography.decode(information[4][2:-1]), self.criptography.decode(information[5][2:-1]), self.criptography.decode(information[6][2:-1]), self.criptography.decode(information[7][2:-1]),
                    self.criptography.decode(information[8][2:-1]), self.criptography.decode(information[9][2:-1]), self.criptography.decode(information[10][2:-1]), self.criptography.decode(information[11][2:-1]),
                    information[11].upper(), information[13].upper()
                )
            )
        return informationsDecode

    def calculing_percentage_for_payment(self, invoicing, percentage):
        if self.validation(infos=[invoicing], type_validation=8) and self.validation(infos=[percentage], type_validation=7) and invoicing != '' and percentage != '':
            invoicingFloat = self.treating_numbers(info=invoicing, type_treating=7)
            percentageFloat = self.treating_numbers(info=percentage, type_treating=7)
            payment = invoicingFloat * (percentageFloat / 100)
            return 'R$' + f'{payment:.2f}'.replace('.', ',')
        else:
            return ''


class FunctionsOfSchedule(GeneralFunctions):

    def register_schedule(self, informations, treeview):
        # informations of treeview ====================
        if self.validation(informations[0:7], 5) and self.validation(informations[2], 4) and self.validation(informations[6], 3) and self.validation(informations[5], 3):
            if self.message_window(4, 'Comfimação', 'Você tem certeza de que deseja cadastrar o atendimento'):
                self.dataBases['schedule'].crud(
                    registerScheduling.format(
                        informations[0].upper(), informations[1].upper(), self.treating_numbers(informations[2], 1), informations[3].upper(), informations[4].upper(),
                        informations[5], self.treating_numbers(informations[6], 3), datetime.today().strftime('%d/%m/%Y  %H:%M'), informations[8].upper(),
                        datetime.today().strftime('%d/%m/%Y  %H:%M') if informations[3] != 'NOTA' else 'SEM PAGAMENTO'
                    ))
                # deleting and inserting informations in treeview ===============================
                self.search_schedule(treeview, informations, 'last', save_seacrh=False)

                self.message_window(1, 'Concluído', messagein=f'Agendamento(s) feito com sucesso')
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_schedule(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['schedule'] = searchSchedule.format(
                'ID' if informations[0].isnumeric() else 'cliente', informations[0], informations[1], informations[2], informations[3], informations[4],
                informations[5], informations[6], informations[7], informations[8], informations[9].replace(' ', '_').lower()
            )

        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['schedule'].searchDatabase(
                    searchSchedule.format(
                        'ID' if informations[0].isnumeric() else 'cliente', informations[0], informations[1], informations[2], informations[3], informations[4],
                        informations[5], informations[6], informations[7], informations[8],  informations[9].replace(' ', '_').lower()
                    )
                )
            case 'last':
                informationsDataBase = self.dataBases['schedule'].searchDatabase(self.lastSearch['schedule'])
            case 'all':
                informationsDataBase = self.dataBases['schedule'].searchDatabase(searchAll.format('Agenda'))
            case 'resumeForCash':
                informationsDataBase = self.dataBases['schedule'].searchDatabase(
                    searchScheduleResume.format(
                        informations[0], informations[1], informations[2], informations[3], informations[4].replace('T/', '').replace(':', '').upper(),
                        informations[5], informations[6], 'horário'
                    )
                )
        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'schedule')
            self.insert_treeview_informations(treeview, informationsDataBase, 'schedule')
        else:
            return informationsDataBase

    def update_schedule(self, treeview, informations):
        # update informations =========================================
        if self.validation(informations, 1) and self.validation(informations[2], 4) and self.validation(informations[6], 3):
            if treeview.selection():
                informationsDataBase = self.dataBases['schedule'].crud(
                    updateSchedule.format(
                        informations[0].upper(), informations[1].upper(), self.treating_numbers(informations[2], 1), informations[3].upper(), informations[4].upper(),
                        informations[5].upper(), self.treating_numbers(informations[6], 3), informations[7].upper(), informations[8].upper(),
                        datetime.today().strftime('%d/%m/%Y  %H:%M') if informations[3] != 'NOTA' else 'SEM PAGAMENTO', self.selection_treeview(treeview)[0][0]
                    )
                )
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'schedule')

                # insert informations in treeview ===============================
                self.search_schedule(treeview, informations, 'last', save_seacrh=False)

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'agendamento(s) atualizado(s) com sucesso')
            else:
                self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def delete_schedule(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'schedule', 'Agenda')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'schedule')

                # insert informations in treeview ===============================
                self.search_schedule(treeview, type_search='last', save_seacrh=False)

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'agendamento(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_schedule(self, treeview):
        informationsTreeview = self.pick_informations_treeview(treeview)
        if informationsTreeview:
            # Collecting informations for messege===============================
            amountClients = len(informationsTreeview)
            sumValue = self.treating_numbers(type_treating=2, values=informationsTreeview)
            methoPay = {
                'card': [row for row in informationsTreeview if row[5] in ['CARTÃO', 'CARTAO']],
                'money': [row for row in informationsTreeview if row[5] in ['DINHEIRO']],
                'transfer': [row for row in informationsTreeview if row[5] in ['TRANSFERÊNCIA', 'TRANSFERENCIA']],
                'note': [row for row in informationsTreeview if row[5] in ['NOTA', 'FIADO', 'NOTINHA']],
                'permute': [row for row in informationsTreeview if row[4] in ['PERMUTA', 'permuta']],
                'vale': [row for row in informationsTreeview if row[4] in ['VALE', 'vale']],
                'notPay': [row for row in informationsTreeview if row[5] in ['NÃO FOI PAGO', 'SEM PAGAMENTO', 'NÃO PAGO', '']],
            }

            sumMetohdPay = [
                amountClients,
                self.treating_numbers(type_treating=2, values=methoPay["card"]),
                self.treating_numbers(type_treating=2, values=methoPay["money"]),
                self.treating_numbers(type_treating=2, values=methoPay["transfer"]),
                self.treating_numbers(type_treating=2, values=methoPay["note"]),
                self.treating_numbers(type_treating=2, values=methoPay["permute"]),
                self.treating_numbers(type_treating=2, values=methoPay["vale"]),
                self.treating_numbers(type_treating=2, values=methoPay["notPay"]),
                sumValue
            ]

            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsScheduleTreeview1.append(information[0:5])
            for information in informationsTreeview:
                tableWithInformationsScheduleTreeview2.append([information[5], information[6], information[7], information[8], information[10]])
            tableWithInformationsComplementarySchedule.append(sumMetohdPay)

            # create tables ===========================================
            table1 = Table(tableWithInformationsScheduleTreeview1)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsScheduleTreeview2)
            table2.setStyle(TableStyle(styleTableInformationsTreeview))
            table3 = Table(tableWithInformationsComplementarySchedule)
            table3.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del tableWithInformationsScheduleTreeview1[2:]
            del tableWithInformationsScheduleTreeview2[2:]
            del tableWithInformationsComplementarySchedule[2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2, table3])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_schedule(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # Collecting informations for messege===============================
            amountClients = len(informationsTreeview)
            sumValues = self.treating_numbers(type_treating=2, values=informationsTreeview)
            methoPay = {
                'card': [row for row in informationsTreeview if row[4] in ['CARTÃO', 'CARTAO']],
                'money': [row for row in informationsTreeview if row[4] in ['DINHEIRO']],
                'transfer': [row for row in informationsTreeview if row[4] in ['TRANSFERÊNCIA', 'TRANSFERENCIA']],
                'note': [row for row in informationsTreeview if row[4] in ['NOTA', 'FIADO', 'NOTINHA']],
                'permute': [row for row in informationsTreeview if row[4] in ['PERMUTA', 'permuta']],
                'vale': [row for row in informationsTreeview if row[4] in ['VALE', 'vale']],
                'notPay': [row for row in informationsTreeview if row[4] in ['NÃO FOI PAGO', 'SEM PAGAMENTO', 'NÃO PAGO', '']],
            }

            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de clientes = {amountClients}\n'
                f'Total em cartão = {self.treating_numbers(type_treating=2, values=methoPay["card"])}\n'
                f'Total em dinheiro = {self.treating_numbers(type_treating=2, values=methoPay["money"])}\n'
                f'Total em tranferència = {self.treating_numbers(type_treating=2, values=methoPay["transfer"])}\n'
                f'Total em nota = {self.treating_numbers(type_treating=2, values=methoPay["note"])}\n'
                f'Total em permuta = {self.treating_numbers(type_treating=2, values=methoPay["permute"])}\n'
                f'Total em vale = {self.treating_numbers(type_treating=2, values=methoPay["vale"])}\n'
                f'Total não pago = {self.treating_numbers(type_treating=2, values=methoPay["notPay"])}\n'
                f'Total recebido = {sumValues}'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')


class FunctionsOfCustomsInformations(GeneralFunctions):

    def register_client(self, informations, treeview, button):
        client = self.dataBases['informations'].searchDatabase(f'SELECT nome FROM Clientes WHERE nome = "{informations[0].upper()}"')
        if not client:
            if self.message_window(4, 'Comfimação', f'Finalisar o cadastro de {informations[0].title()}?'):
                # informations of treeview ====================
                self.dataBases['informations'].crud(
                    registerClient.format(
                        informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(),
                        informations[6].upper(), informations[7].upper(), informations[8].upper(), informations[9].upper(), informations[10].upper(), informations[11], informations[12].upper()
                    )
                )
                # deleting and inserting informations in treeview ===============================
                self.search_client(treeview, informations, 'all', save_seacrh=False)
                button.invoke()

                # refresh =======================================================
                self.refresh_combobox_client()
        else:
            self.message_window(2, 'Já cadastrado', f'{informations[0].title()} Já esta cadastrado')

    def search_client(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['client'] = searchClient.format(
                'ID' if informations[0].isnumeric() else 'nome',
                informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(),
                informations[6].upper(), informations[7].upper(), informations[8].upper(), informations[9].upper(), informations[10].upper(), informations[12].upper(), informations[13].replace(' ', '_')
            )
        # pick up informations =========================================
        informationsDatabase = []
        match type_search:
            case 'new':
                informationsDatabase = self.dataBases['informations'].searchDatabase(
                    searchClient.format(
                        'ID' if informations[0].isnumeric() else 'nome',
                        informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(),
                        informations[6].upper(), informations[7].upper(), informations[8].upper(), informations[9].upper(), informations[10].upper(), informations[12].upper(), informations[13].replace(' ', '_')
                    )
                )
            case 'last':
                informationsDatabase = self.dataBases['informations'].searchDatabase(self.lastSearch['client'])
            case 'all':
                informationsDatabase = self.dataBases['informations'].searchDatabase(searchAll.format('Clientes'))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'client')
            self.insert_treeview_informations(treeview, informationsDatabase, 'client')
        else:
            return informationsDatabase

    def update_client(self, treeview, informations, entrys):
        # update informations =========================================
        if treeview.selection():
            informationsDataBase = self.dataBases['informations'].crud(
                updateClient.format(
                    informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(), informations[6].upper(),
                    informations[7].upper(), informations[8].upper(), informations[9].upper(), informations[10].upper(), informations[11], informations[12].upper(), self.selection_treeview(treeview)[0][0]
                )
            )
            # delete informations of treeview ==============================
            self.delete_informations_treeview(treeview, 'client')

            # insert informations in treeview ===============================
            self.search_client(treeview, informations, 'last', save_seacrh=False)

            # refresh =======================================================
            self.refresh_combobox_client()

            # show message of concluded
            self.message_window(1, 'Concluído', messagein=f'Cadastro de {informations[0].title()} atualizado com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')

    def delete_client(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'informations', 'Clientes')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'client')

                # insert informations in treeview ===============================
                self.search_client(treeview, type_search='last', save_seacrh=False)

                # refresh =======================================================
                self.refresh_combobox_client()

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Cadastro(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_client(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # Collecting informations for messege===============================
            informationsComplementary = [
                len(informationsTreeview),
                len([row for row in informationsTreeview if row[4] == 'SIM']),
                len([row for row in informationsTreeview if row[4] == 'NÃO']),
                len([row for row in informationsTreeview if row[10] in ['BELO CAMPO', 'belo campo']]),
                len([row for row in informationsTreeview if row[10] not in ['BELO CAMPO', 'belo campo']]),
            ]

            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsClientTreeview1.append(information[0:6])
            for information in informationsTreeview:
                tableWithInformationsClientTreeview2.append(information[6:12])
            tableWithInformationsComplementaryClient.append(informationsComplementary)

            # create tables ===========================================
            table1 = Table(tableWithInformationsClientTreeview1)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsClientTreeview2)
            table2.setStyle(TableStyle(styleTableInformationsTreeview))
            table3 = Table(tableWithInformationsComplementaryClient)
            table3.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del tableWithInformationsClientTreeview1[2:]
            del tableWithInformationsClientTreeview2[2:]
            del tableWithInformationsComplementaryClient[2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2, table3])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_clients(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # Collecting informations for messege===============================
            amountClients = len(informationsTreeview)
            informationsComplementary = {
                'children': [row for row in informationsTreeview if row[4] == 'SIM'],
                'notChildren': [row for row in informationsTreeview if row[4] == 'NÃO'],
                'residents': [row for row in informationsTreeview if row[10] in ['BELO CAMPO', 'belo campo']],
                'visitors': [row for row in informationsTreeview if row[10] not in ['BELO CAMPO', 'belo campo']],
            }

            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de clientes = {amountClients}\n'
                f'Pais = {len(informationsComplementary["children"])}\n'
                f'Sem filhos = {len(informationsComplementary["notChildren"])}\n'
                f'Moradores = {len(informationsComplementary["residents"])}\n'
                f'Visitantes = {len(informationsComplementary["visitors"])}\n'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def refresh_combobox_client(self):
        # refresh list of combobox services ================================
        self.customScheduleEntry.configure(values=[name[1] for name in self.search_client(informations=self.searching_list('', 12, 'nome'), save_seacrh=False, insert=False)])
        self.customSaleInventoryControlEntry.configure(values=[name[1] for name in self.search_client(informations=self.searching_list('', 12, 'nome'), save_seacrh=False, insert=False)])
        self.customSaleInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_client(informations=self.searching_list('', 12, 'nome'), save_seacrh=False, insert=False)])


class FunctionsOfProfessionalInformations(GeneralFunctions):

    def register_professional(self, informations, treeview, button):
        professional = self.dataBases['informations'].searchDatabase(f'SELECT nome FROM Profissionais WHERE nome = "{informations[0].upper()}"')
        if not professional:
            if self.message_window(4, 'Comfimação', f'Finalisar o cadastro de {informations[0].title()}?'):
                # informations of treeview ====================
                self.dataBases['informations'].crud(
                    registerProfessional.format(
                        informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(),
                        informations[6].upper(), informations[7].upper(), informations[8].upper(), informations[9].upper(), informations[10].upper(), informations[11], informations[12].upper()
                    ))
                # deleting and inserting informations in treeview ===============================
                self.search_professional(treeview, informations, 'all', save_seacrh=False)
                button.invoke()
                # refresh =======================================================
                self.refresh_combobox_professional()
        else:
            self.message_window(2, 'Já cadastrado', f'{informations[0].title()} Já esta cadastrado')

    def search_professional(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['employee'] = searchProfessional.format(
                'ID' if informations[0].isnumeric() else 'nome', informations[0], informations[1], informations[2], informations[3], informations[4],
                informations[5], informations[6], informations[7], informations[8], informations[9], informations[10], informations[12], informations[13].replace('-', '_')
            )
        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['informations'].searchDatabase(
                    searchProfessional.format(
                        'ID' if informations[0].isnumeric() else 'nome', informations[0], informations[1], informations[2], informations[3], informations[4],
                        informations[5], informations[6], informations[7], informations[8], informations[9], informations[10], informations[12], informations[13].replace('-', '_')
                    )
                )
            case 'last':
                informationsDataBase = self.dataBases['informations'].searchDatabase(self.lastSearch['employee'])
            case 'all':
                informationsDataBase = self.dataBases['informations'].searchDatabase(searchAll.format('Profissionais'))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'employee')
            self.insert_treeview_informations(treeview, informationsDataBase, 'employee')
        else:
            return informationsDataBase

    def update_professional(self, treeview, informations):
        # update informations =========================================
        if treeview.selection():
            informationsDataBase = self.dataBases['informations'].crud(
                updateProfessional.format(
                    informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(), informations[6].upper(),
                    informations[7].upper(), informations[8].upper(), informations[9].upper(), informations[10].upper(), informations[11], informations[12].upper(), self.selection_treeview(treeview)[0][0]
                )
            )
            # delete informations of treeview ==============================
            self.delete_informations_treeview(treeview, 'employee')

            # insert informations in treeview ===============================
            self.search_professional(treeview, informations, 'last', save_seacrh=False)

            # refresh =======================================================
            self.refresh_combobox_professional()

            # show message of concluded
            self.message_window(1, 'Concluído', messagein=f'Cadastro de {informations[0].title()} atualizado com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')

    def delete_professional(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'informations', 'Profissionais')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'employee')

                # insert informations in treeview ===============================
                self.search_professional(treeview, type_search='last', save_seacrh=False)

                # refresh =======================================================
                self.refresh_combobox_professional()

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Cadastro(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_professional(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # Collecting informations for messege===============================
            informationsComplementary = [
                len(informationsTreeview),
            ]

            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsProfesiionalTreeview1.append(information[0:6])
            for information in informationsTreeview:
                tableWithInformationsProfesiionalTreeview2.append(information[6:12])
            tableWithInformationsComplementaryProfesiional.append(informationsComplementary)

            # create tables ===========================================
            table1 = Table(tableWithInformationsProfesiionalTreeview1)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsProfesiionalTreeview2)
            table2.setStyle(TableStyle(styleTableInformationsTreeview))
            table3 = Table(tableWithInformationsComplementaryProfesiional)
            table3.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del tableWithInformationsProfesiionalTreeview1[2:]
            del tableWithInformationsProfesiionalTreeview2[2:]
            del tableWithInformationsComplementaryProfesiional[2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2, table3])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_professional(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # Collecting informations for messege ===============================
            amountProfessional = len(informationsTreeview)

            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de Profissionais = {amountProfessional}\n'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def refresh_combobox_professional(self):
        # refresh list of combobox services ================================
        self.professionalScheduleEntry.configure(values=[name[1] for name in self.search_professional(informations=self.searching_list('', 12, 'nome'), save_seacrh=False, insert=False)])
        self.employeeCashPayEntry.configure(values=[name[1] for name in self.search_professional(informations=self.searching_list('', 12, 'nome'), save_seacrh=False, insert=False)])


class FunctionsOfServiceInformations(GeneralFunctions):

    def register_service(self, informations, treeview, button):
        if self.validation(informations, 5) and self.validation(self.treating_numbers(informations[1], 1), 4, 1):
            if self.message_window(4, 'Comfimação', f'Finalisar o cadastro de serviço?'):
                # informations of treeview ====================
                self.dataBases['informations'].crud(registerServices.format(informations[0].upper(), self.treating_numbers(informations[1], 1)))
                # deleting and inserting informations in treeview ===============================
                self.search_service(treeview, informations, "last", save_seacrh=False)
                button.invoke()
                # refresh list =============================
                self.refresh_combobox_service()
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_service(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['service'] = searchServices.format('ID' if informations[0].isnumeric() else 'serviço', informations[0], informations[1], "serviço")
        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['informations'].searchDatabase(searchServices.format('ID' if informations[0].isnumeric() else 'serviço', informations[0], informations[1], "serviço"))
            case 'last':
                informationsDataBase = self.dataBases['informations'].searchDatabase(self.lastSearch['service'])
            case 'all':
                informationsDataBase = self.dataBases['informations'].searchDatabase(searchAll.format('Serviços'))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'service')
            self.insert_treeview_informations(treeview, informationsDataBase, 'service')
        else:
            return informationsDataBase

    def update_service(self, treeview, informations):
        if self.validation(informations, 5) and self.validation(self.treating_numbers(informations[1], 1), 4, 1):
            # update informations =========================================
            if treeview.selection():
                informationsDataBase = self.dataBases['informations'].crud(updateService.format(informations[0].upper(), self.treating_numbers(informations[1], 1), self.selection_treeview(treeview)[0][0]))
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'service')

                # insert informations in treeview ===============================
                self.search_service(treeview, type_search='last', save_seacrh=False)

                # refresh list =============================
                self.refresh_combobox_service()

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'Serviço de {informations[0].title()} atualizado com sucesso')
            else:
                self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def delete_service(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'informations', 'Serviços')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'service')

                # insert informations in treeview ===============================
                self.search_service(treeview, type_search='last', save_seacrh=False)

                # refresh list =============================
                self.refresh_combobox_service()

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Serviço(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_service(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsServiceTreeview.append(information)
            tableWithInformationsComplementaryService.append([len(informationsTreeview)])

            # create tables ===========================================
            table1 = Table(tableWithInformationsServiceTreeview)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsComplementaryService)
            table2.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del tableWithInformationsServiceTreeview[2:]
            del tableWithInformationsComplementaryService[2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_service(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de serviços = {len(informationsTreeview)}\n'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def refresh_combobox_service(self):
        # refresh list of combobox services ================================
        self.serviceScheduleEntry.configure(values=[name[1] for name in self.search_service(informations=self.searching_list('', 1, 'serviço'), save_seacrh=False, insert=False)])


class FunctionsOfBarCodeInformations(GeneralFunctions):

    def register_barCode(self, informations, treeview, button):
        if self.validation(informations[0:3], 5) and self.validation(informations[2], 6):
            if self.message_window(4, 'Comfimação', f'Finalisar o cadastro do código?'):
                # creating bar code ===========================
                directoryBarCode = self.create_image_barCode(informations)
                if directoryBarCode[0] != '.png':
                    # registing ====================
                    self.dataBases['informations'].crud(
                        registerBarCode.format(informations[0].upper(), informations[1].upper(), directoryBarCode[1], directoryBarCode[0], informations[3])
                    )
                    # deleting and inserting informations in treeview ===============================
                    self.search_barCode(treeview, informations, 'all', save_seacrh=False)
                    button.invoke()
                    # refresh list =============================
                    self.refresh_combobox_barCode()
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_barCode(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['barCode'] = searchBarCode.format('ID' if informations[0].isnumeric() else 'profissional', informations[0], informations[1], informations[2], informations[3], informations[4])
        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['informations'].searchDatabase(searchBarCode.format('ID' if informations[0].isnumeric() else 'profissional', informations[0], informations[1], informations[2], informations[3], informations[4]))
            case 'last':
                informationsDataBase = self.dataBases['informations'].searchDatabase(self.lastSearch['barCode'])
            case 'all':
                informationsDataBase = self.dataBases['informations'].searchDatabase(searchAll.format('Código_de_barras'))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'barCode')
            self.insert_treeview_informations(treeview, informationsDataBase, 'barCode')
        else:
            return informationsDataBase

    def update_barCode(self, treeview, informations):
        if self.validation(informations[0:2], 5):
            if treeview.selection():
                # update informations =========================================
                informationsDataBase = self.dataBases['informations'].crud(
                    updateBarCode.format(informations[0].upper(), informations[1].upper(), informations[3].upper(), self.selection_treeview(treeview)[0][0])
                )

                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'barCode')

                # insert informations in treeview ===============================
                self.search_barCode(treeview, type_search='last', save_seacrh=False)

                # refresh list =============================
                self.refresh_combobox_barCode()

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'Código de atualizado com sucesso')
            else:
                self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def delete_barCode(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'informations', 'Código_de_barras')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'barCode')

                # insert informations in treeview ===============================
                self.search_barCode(treeview, type_search='last', save_seacrh=False)

                # refresh list =============================
                self.refresh_combobox_barCode()

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'código(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    @staticmethod
    def create_image_barCode(informations):
        # creating file name ========================================
        fileName = f'{informations[0].capitalize()}={informations[1].capitalize()}'
        # creating image of bar code ================================
        code = EAN13(informations[2])
        # saving image ==============================================
        directory = filedialog.askdirectory(initialdir='Documentos', title='Selecione aonde salvar o código de barras')
        directoryCompleted = ''
        if directory != '':
            directoryCompleted = rf'{directory}/{fileName}'
            code.save(directoryCompleted)
            # open image for tranform in png and drawing ============================================
            cairosvg.svg2png(url=directoryCompleted + '.svg', write_to=directoryCompleted + '.png', output_width=523, output_height=280)
            os.remove(directoryCompleted + '.svg')
            image = Image.open(directoryCompleted + '.png')
            # creating new image for paste and writing in the image ===============================
            new_image = Image.new('RGB', (523, 380), color='white')
            # calculating coordenades for centralize image in the image ==========================
            x = (523 - image.width) // 2
            y = (380 - image.height) // 2
            new_image.paste(image, (x, y))
            draw = ImageDraw.Draw(new_image)
            # setting a font writing ====================================================
            font = ImageFont.truetype('assets/font.otf', 60)
            # positioning and drawing text in image ========================================
            fileNameReplace = fileName.replace('=', ' -> ')
            largura, altura = new_image.size
            texto_largura = draw.textlength(fileNameReplace, font)
            texto_altura = font.size
            posicao = ((largura - texto_largura) // 2, (altura - texto_altura) // 2 + 145)
            draw.text(posicao, fileNameReplace, font=font, fill=(242, 56, 205))
            # saving the image ===========================================================
            new_image.save(directoryCompleted + '.png')
            new_image.close()

        return [directoryCompleted + '.png', code.get_fullcode()]

    def create_image_colage(self):
        folderImages = filedialog.askdirectory(title='Selecione a pasta com as imagens')
        if folderImages != '':
            listBarCodes = [os.path.join(f'{folderImages}', foto) for foto in os.listdir(f'{folderImages}')]

            if len(listBarCodes) > 4:
                saveDirectory = filedialog.asksaveasfilename(defaultextension="*.png ", filetypes=[('Arquivos de png', "*.png")])
                if saveDirectory is not None:
                    cola = create_collage(
                        lst=listBarCodes,
                        width=1000,
                        background=(255, 255, 255),
                        save_path=f'{saveDirectory}',
                    )
                    self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
            else:
                self.message_window(2, 'Imagens insuficientes', 'Tenha no mínimo 4 imagens para a colagem')

    def create_pdf_barCode(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsBarCodeTreeview.append(information[0:4])
            tableWithInformationsComplementaryBarCode.append([len(informationsTreeview)])

            # create tables ===========================================
            table1 = Table(tableWithInformationsBarCodeTreeview)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsComplementaryBarCode)
            table2.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del tableWithInformationsBarCodeTreeview[2:]
            del tableWithInformationsComplementaryBarCode[2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_barCode(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de serviços = {len(informationsTreeview)}\n'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def refresh_combobox_barCode(self):
        # refresh list of combobox services ================================
        self.cheatScheduleEntry.configure(values=[name[3] for name in self.search_barCode(informations=self.searching_list('', 3, 'código'), save_seacrh=False, insert=False)])


class FunctionsOfInformationsStock(GeneralFunctions):

    def register_InformationsStock(self, informations, treeview, button):
        if informations[1] != "":
            if self.message_window(4, 'Comfimação', f'Finalisar o cadastro da informação?'):
                # informations of treeview ====================
                self.dataBases['informations'].crud(registerInformationsOfStock.format(informations[0], informations[0].lower(), informations[1].upper()))
                # deleting and inserting informations in treeview ===============================
                self.search_InformationsStock(treeview, informations, 'all', typeInformations=informations[3], table=informations[0], save_seacrh=False)
                button.invoke()
                # refresh list =============================
                self.refresh_combobox_InformationsStock()
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_InformationsStock(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True, **kwargs):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch[kwargs['typeInformations']] = searchInformationsOfStock.format(informations[0], 'ID' if informations[0].isnumeric() else informations[0].lower(), informations[1], informations[2])
        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['informations'].searchDatabase(
                    searchInformationsOfStock.format(informations[0], 'ID' if informations[0].isnumeric() else informations[0].lower(), informations[1], informations[2])
                )
            case 'last':
                informationsDataBase = self.dataBases['informations'].searchDatabase(self.lastSearch[kwargs['typeInformations']])
            case 'all':
                informationsDataBase = self.dataBases['informations'].searchDatabase(searchAll.format(kwargs['table']))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, kwargs['typeInformations'])
            self.insert_treeview_informations(treeview, informationsDataBase, kwargs['typeInformations'])
        else:
            return informationsDataBase

    def update_InformationsStock(self, treeview, informations, **kwargs):
        if informations[1] != '':
            # update informations =========================================
            if treeview.selection():
                informationsDataBase = self.dataBases['informations'].crud(updateInformationsOfStock.format(informations[0], informations[0].lower(), informations[1].upper(), self.selection_treeview(treeview)[0][0]))
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, kwargs['typeInformations'])

                # insert informations in treeview ===============================
                self.search_InformationsStock(treeview, type_search='last', save_seacrh=False, typeInformations=kwargs['typeInformations'])

                # refresh list =============================
                self.refresh_combobox_InformationsStock()

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'Informação atualizada com sucesso')
            else:
                self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')
        else:
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def delete_InformationsStock(self, treeview, informations, **kwargs):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'informations', kwargs['table'])

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, kwargs['typeInformations'])

                # insert informations in treeview ===============================
                self.search_InformationsStock(treeview, type_search='last', save_seacrh=False, typeInformations=kwargs['typeInformations'])

                # refresh list =============================
                self.refresh_combobox_InformationsStock()

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Infoemações(s) deletada(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_InformationsStock(self, treeview, information):
        if informationsTreeview := self.pick_informations_treeview(treeview):

            # tables ============================================
            tableWithInformationsStockTreeview = [['', ''], ['ID', f'{information}']]
            tableWithInformationsComplementaryInformationsStock = [[''], [f'Total de {information}']]

            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsStockTreeview.append(information)
            tableWithInformationsComplementaryInformationsStock.append([len(informationsTreeview)])

            # create tables ===========================================
            table1 = Table(tableWithInformationsStockTreeview)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsComplementaryInformationsStock)
            table2.setStyle(TableStyle(styleTableInformationsComplementary))

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_InformationsStock(self, treeview, infotmation):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de {infotmation} = {len(informationsTreeview)}\n'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def refresh_combobox_InformationsStock(self):
        # refresh list of combobox informations ================================
        # supplier ---------------------------------
        self.supplierUseInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Fornecedor', 1, 'Fornecedor'), save_seacrh=False, insert=False)])
        self.supplierUseInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Fornecedor', 1, 'Fornecedor'), save_seacrh=False, insert=False)])
        self.supplierSaleInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Fornecedor', 1, 'Fornecedor'), save_seacrh=False, insert=False)])
        self.supplierSaleInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Fornecedor', 1, 'Fornecedor'), save_seacrh=False, insert=False)])
        # brand ------------------------------------
        self.brandUseInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Marca', 1, 'Marca'), save_seacrh=False, insert=False)])
        self.brandSaleInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Marca', 1, 'Marca'), save_seacrh=False, insert=False)])
        self.brandUseInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Marca', 1, 'Marca'), save_seacrh=False, insert=False)])
        self.brandSaleInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Marca', 1, 'Marca'), save_seacrh=False, insert=False)])
        # type -------------------------------------
        self.typeUseInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Tipo', 1, 'Tipo'), save_seacrh=False, insert=False)])
        self.typeSaleInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Tipo', 1, 'Tipo'), save_seacrh=False, insert=False)])
        self.typeUseInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Tipo', 1, 'Tipo'), save_seacrh=False, insert=False)])
        self.typeSaleInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Tipo', 1, 'Tipo'), save_seacrh=False, insert=False)])
        # measure -------------------------------------
        self.measureUseInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Medida', 1, 'Medida'), save_seacrh=False, insert=False)])
        self.measureSaleInventoryControlEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Medida', 1, 'Medida'), save_seacrh=False, insert=False)])
        self.measureUseInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Medida', 1, 'Medida'), save_seacrh=False, insert=False)])
        self.measureSaleInventoryControlUnusableEntry.configure(values=[name[1] for name in self.search_InformationsStock(informations=self.searching_list('Medida', 1, 'Medida'), save_seacrh=False, insert=False)])

    def search_init(self):
        self.search_InformationsStock(self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor')
        self.search_InformationsStock(self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca')
        self.search_InformationsStock(self.type['treeview'], ['Tipo', self.type['entry'].get(), self.type['order'].get()], typeInformations='type', table='Tipo')
        self.search_InformationsStock(self.measure['treeview'], ['Medida', self.measure['entry'].get(), self.measure['order'].get()], typeInformations='measure', table='Medida')


class FunctionsOfStockInformations(GeneralFunctions):

    def register_stock(self, informations, treeview, delete=False, **kwargs):
        # register usage stock ====================
        if kwargs['sqlRegister'] == registerUsageStock:
            if self.validation(informations[0:7], 5) and self.validation(informations[3], 3) and self.validation(self.treating_numbers(informations[5], 1), 4):
                if self.message_window(4, 'Comfimação', f'Finalisar o cadastro do produto?'):
                    self.dataBases['stock'].crud(
                        kwargs['sqlRegister'].format(
                            informations[0].upper(), informations[1].upper(), informations[2].upper(), '0' if informations[3] == '' else informations[3],
                            informations[4].upper(), self.treating_numbers(informations[5], 1), informations[6], '0' if informations[7] == '' else informations[7],
                            informations[3] if informations[8] == '' else informations[8], datetime.today().strftime('%d/%m/%Y  %H:%M') if informations[9] == '' else informations[9].upper(),
                            datetime.today().strftime('%d/%m/%Y  %H:%M') if informations[10] == '' else informations[10].upper(), informations[11], informations[12].upper()
                        ))
                    # deleting and inserting informations in treeview ===============================
                    self.search_stock(treeview, informations, 'all', table=kwargs['table'], save_seacrh=False, typeStock=kwargs['typeStock'])
                    kwargs['button'].invoke()
            else:
                # show message error =====================================================
                self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')
        # register sale stock ====================
        elif kwargs['sqlRegister'] in [registerSaleStock, registerSaleStockUnusable]:
            # treating numbers ==========================
            valuesPrice = [self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1)]
            if self.validation(informations[0:8], 5) and self.validation(informations[3], 3) and self.validation(valuesPrice[0], 4) and self.validation(valuesPrice[1], 4):
                if self.message_window(4, 'Comfimação', f'Finalisar o cadastro do produto?'):
                    self.dataBases['stock'].crud(
                        kwargs['sqlRegister'].format(
                            informations[0].upper(), informations[1].upper(), informations[2].upper(), '0' if informations[3] == '' else informations[3],
                            informations[4].upper(), self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1), informations[7],
                            'NENHUM' if informations[8] == '' else informations[8], 'SEM PAGAMENTO' if informations[9] == '' else informations[9].upper(),
                            datetime.today().strftime('%d/%m/%Y  %H:%M') if informations[10] == '' else informations[10].upper(), informations[11], informations[12], datetime.today().strftime('%d/%m/%Y  %H:%M')
                        ))
                    # deleting and inserting informations in treeview ===============================
                    self.search_stock(treeview, informations, 'allSale', table=kwargs['table'], save_seacrh=False, typeStock=kwargs['typeStock'], column=kwargs['column'])
                    if delete:
                        self.delete_stock(self.treeviewSaleInventoryControl, parameters={'table': 'Estoque_de_vendidos', 'typeStock': 'productSaleSold', 'column': 'venda'})
                    kwargs['button'].invoke()
            else:
                # show message error =====================================================
                self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_stock(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True, **kwargs):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch[kwargs['typeStock']] = kwargs['sqlSearch'].format(
                informations[0], informations[1], informations[2], informations[3], informations[4],
                informations[5], informations[6], informations[7], informations[8], informations[9],
                informations[10], informations[12], informations[13].replace('Q/', '').replace('V/', 'valor_de_').replace('D/', 'data_de_').replace(' ', '_').lower()
            )
        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['stock'].searchDatabase(
                    kwargs['sqlSearch'].format(
                        informations[0], informations[1], informations[2], informations[3], informations[4],
                        informations[5], informations[6], informations[7], informations[8], informations[9],
                        informations[10], informations[12], informations[13].replace('Q/', '').replace('V/', 'valor_de_').replace('D/', 'data_de_').replace(' ', '_').lower()
                    )
                )
            case 'last':
                informationsDataBase = self.dataBases['stock'].searchDatabase(self.lastSearch[kwargs['typeStock']])
            case 'all':
                informationsDataBase = self.dataBases['stock'].searchDatabase(searchAll.format(kwargs['table']))
            case 'allSale':
                informationsDataBase = self.dataBases['stock'].searchDatabase(searchAllForSale.format(kwargs['column'], kwargs['table']))
            case 'resumeForCash':
                informationsDataBase = self.dataBases['stock'].searchDatabase(
                    searchSoldStockResumeForCash.format(
                        informations[0], informations[1], informations[2], informations[3], informations[4],
                        informations[5], informations[6].replace('T/', '').replace(':', '').upper(), informations[7], 'venda'
                    )
                )

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, kwargs['typeStock'])
            self.insert_treeview_informations(treeview, informationsDataBase, kwargs['typeStock'])
        else:
            return informationsDataBase

    def update_stock(self, treeview, informations, parameters):
        # update informations =========================================
        if treeview.selection():
            if parameters['sqlUpdate'] == updateUsageStock or parameters['sqlUpdate'] == updateUsageStockUnusable:
                if self.validation(informations[0:7], 5) and self.validation(informations[3], 3) and self.validation(self.treating_numbers(informations[5], 1), 4):
                    self.dataBases['stock'].crud(
                        parameters['sqlUpdate'].format(
                            informations[0].upper(), informations[1].upper(), informations[2].upper(), '0' if informations[3] == '' else informations[3],
                            informations[4].upper(), self.treating_numbers(informations[5], 1), informations[6], "0" if informations[7] == '' else informations[7],
                            int(informations[8]) - int(informations[7]), datetime.today().strftime('%d/%m/%Y  %H:%M') if informations[9] == '' else informations[9].upper(),
                            datetime.today().strftime('%d/%m/%Y  %H:%M'), informations[11], informations[12].upper(), self.selection_treeview(treeview)[0][0]
                        )
                    )
                    search = self.dataBases['stock'].searchDatabase(f'SELECT quantidade, restante FROM {parameters["table"]} WHERE ID = {self.selection_treeview(treeview)[0][0]}')[0]
                    self.dataBases['stock'].crud(f'UPDATE {parameters["table"]} SET saída = {int(search[0]) - int(search[1])}')
                    # delete informations of treeview ==============================
                    self.delete_informations_treeview(treeview, parameters['typeStock'])

                    # deleting and inserting informations in treeview ===============================
                    self.search_stock(treeview, informations, 'last', save_seacrh=False, typeStock=parameters['typeStock'])

                    # show message of concluded
                    self.message_window(1, 'Concluído', messagein=f'Produto atualizado com sucesso')
                else:
                    # show message error =====================================================
                    self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')
            elif parameters['sqlUpdate'] in [updateSaleStock, updateSaleStockUnusable]:
                # treating numbers ==========================
                valuesPrice = [self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1)]
                if self.validation(informations[0:8], 5) and self.validation(informations[3], 3) and self.validation(valuesPrice[0], 4) and self.validation(valuesPrice[1], 4):
                    self.dataBases['stock'].crud(
                        parameters['sqlUpdate'].format(
                            informations[0].upper(), informations[1].upper(), informations[2].upper(), '0' if informations[3] == '' else informations[3],
                            informations[4].upper(), self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1), informations[7],
                            'NENHUM' if informations[8] == '' else informations[8], 'SEM PAGAMENTO' if informations[9] == '' else informations[9].upper(),
                            informations[10], informations[11], informations[12].upper(), datetime.today().strftime('%d/%m/%Y  %H:%M'), self.selection_treeview(treeview)[0][0]
                        )
                    )
                    # delete informations of treeview ==============================
                    self.delete_informations_treeview(treeview, parameters['typeStock'])

                    # deleting and inserting informations in treeview ===============================
                    self.search_stock(treeview, informations, 'last', save_seacrh=False, typeStock=parameters['typeStock'])

                    # show message of concluded
                    self.message_window(1, 'Concluído', messagein=f'Produto atualizado com sucesso')
                else:
                    # show message error =====================================================
                    self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')

    def delete_stock(self, treeview, register_in_unusable=False, treeview2=None, parameters=None):
        if treeview.selection():
            if register_in_unusable:
                if self.message_window(4, 'Comfimação', f'Enviar o produto para o estoque inutilizavel?'):
                    informations = self.selection_treeview(treeview)
                    for product in informations:
                        self.dataBases['stock'].crud(
                            registerUsageStockUnusable.format(
                                product[1].upper(), product[2].upper(), product[3].upper(), '0' if product[4] == '' else product[4],
                                product[5].upper(), self.treating_numbers(product[6], 1), product[7], '0' if product[8] == '' else product[8],
                                product[9], datetime.today().strftime('%d/%m/%Y  %H:%M'),
                                datetime.today().strftime('%d/%m/%Y  %H:%M'), product[12], product[13].upper()
                            )
                        )
                    # deleting and inserting informations in treeview ===============================
                    self.search_stock(treeview2, type_search='all', save_seacrh=False, typeStock='productUseUnusable', table='Estoque_de_inutilizáveis')
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'stock', parameters['table'])

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, parameters['typeStock'])

                # deleting and inserting informations in treeview ===============================
                if treeview in [self.treeviewSaleInventoryControl, self.treeviewSaleInventoryControlUnusable]:
                    self.search_stock(treeview, self.searching_list('', 11, 'ID'), 'allSale', table=parameters['table'], save_seacrh=False, typeStock=parameters['typeStock'], column=parameters['column'])
                else:
                    self.search_stock(treeview, type_search='last', save_seacrh=False, typeStock=parameters['typeStock'])

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Produto(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_stock(self, treeview, **kwargs):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # informations ============================================
            for information in informationsTreeview:
                kwargs['tablePart1'].append(information[0:6])
            for information in informationsTreeview:
                kwargs['tablePart2'].append(information[6:12])
            kwargs['supplementaryTable'].append(self.informations_supplementarys(informationsTreeview, kwargs['typeStock']))

            # create tables ===========================================
            table1 = Table(kwargs['tablePart1'])
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(kwargs['tablePart2'])
            table2.setStyle(TableStyle(styleTableInformationsTreeview))
            table3 = Table(kwargs['supplementaryTable'])
            table3.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del kwargs['tablePart1'][2:]
            del kwargs['tablePart2'][2:]
            del kwargs['supplementaryTable'][2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2, table3])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_stock(self, treeview, **kwargs):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # show menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                kwargs['typeMessage'].format(*self.informations_supplementarys(informationsTreeview, kwargs['typeStock']))
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def informations_supplementarys(self, informations, type_stock=''):
        # píck up informations supplementarys ==============================
        match type_stock:
            case 'usageStock':
                defeated = 0
                finished = 0
                for information in informations:
                    date_validity = datetime.strptime(information[7], '%d/%m/%Y')
                    if datetime.now() >= date_validity:
                        defeated += 1
                    if information[9] == '0':
                        finished = 0
                return [len(informations), self.treating_numbers(values=informations, type_treating=2, ide=6), defeated, finished]
            case 'saleStock':
                defeated = 0
                reserved = 0
                for information in informations:
                    date_validity = datetime.strptime(information[8], '%d/%m/%Y')
                    if datetime.now() >= date_validity:
                        defeated += 1
                    if information[9] not in ['NENHUM', '']:
                        reserved += 1
                return [len(informations), self.treating_numbers(values=informations, type_treating=2, ide=6), self.treating_numbers(values=informations, type_treating=2, ide=7), reserved, defeated]

    @staticmethod
    def select_finished_and_defeated(treeview, type_stock):
        match type_stock:
            case 'usageStock':
                for product in treeview.get_children():
                    date_validity = datetime.strptime(treeview.set(product, "Validade"), "%d/%m/%Y")
                    if datetime.now() >= date_validity or int(treeview.set(product, "Q/Restante")) <= 0:
                        treeview.selection_add(product)
            case 'saleStock':
                for product in treeview.get_children():
                    date_validity = datetime.strptime(treeview.set(product, "Validade"), "%d/%m/%Y")
                    if datetime.now() >= date_validity:
                        treeview.selection_add(product)


class FunctionsOfCashManagement(GeneralFunctions):

    def register_cashManagement(self, informations, treeview, button, parameters):
        # register usage stock ====================
        if self.validation(informations[0:8] + [informations[9], informations[10]], 5) and self.validation(informations[0:2], 7) and self.validation(informations[2:10], 8):
            if self.message_window(4, 'Comfimação', f'Registrar os dados?'):
                if treeview == self.treeviewCashDayInformations:
                    self.dataBases['cash'].crud(
                        parameters['sqlRegister'].format(
                            parameters['table'], parameters['typeDate'], informations[0].upper(), informations[1].upper(), self.treating_numbers(informations[2], 1), self.treating_numbers(informations[3], 1),
                            self.treating_numbers(informations[4], 1), self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1), self.treating_numbers(informations[7], 1), 'R$0,00', 'R$0,00', 'R$0,00', 'R$0,00', 'R$0,00',
                            self.treating_numbers(informations[8], 1) if informations[8] != '' else self.treating_numbers('0', 1), self.treating_numbers(informations[9], 1), datetime.today().strftime('%d/%m/%Y') if informations[10] == '' else informations[10],
                            "DIA EM ANDAMENTO"
                        ))
                elif treeview == self.frameTreeviewCashMonth:
                    self.dataBases['cash'].crud(
                        parameters['sqlRegister'].format(
                            parameters['table'], parameters['typeDate'], informations[0].upper(), informations[1].upper(), self.treating_numbers(informations[2], 1), self.treating_numbers(informations[3], 1),
                            self.treating_numbers(informations[4], 1), self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1), 'R$0,00', 'R$0,00', 'R$0,00', 'R$0,00', 'R$0,00',
                            self.treating_numbers(informations[7], 1) if informations[7] != '' else self.treating_numbers('0', 1), self.treating_numbers(informations[8], 1), datetime.today().strftime('%d/%m/%Y') if informations[9] == '' else informations[9],
                            "MÊS EM ANDAMENTO"
                        ))
                else:
                    informationsGeneral = self.calculateDate([informations[9], informations[10]])
                    self.dataBases['cash'].crud(
                        parameters['sqlRegister'].format(
                            parameters['table'], informationsGeneral[0], informationsGeneral[1], self.treating_numbers(informationsGeneral[2], 1), self.treating_numbers(informationsGeneral[3], 1), self.treating_numbers(informationsGeneral[4], 1),
                            self.treating_numbers(informationsGeneral[5], 1), self.treating_numbers(informationsGeneral[6], 1), self.treating_numbers(informationsGeneral[7], 1), self.treating_numbers(informationsGeneral[8], 1), self.treating_numbers(informationsGeneral[9], 1),
                            self.treating_numbers(informationsGeneral[10], 1), self.treating_numbers(informationsGeneral[11], 1), self.treating_numbers(informationsGeneral[12], 1),
                            self.treating_numbers(informationsGeneral[13], 1), f'De {informations[9]} até {informations[10]}', datetime.today().strftime('%d/%m/%Y')
                        ))
                # deleting and inserting informations in treeview ===============================
                button.invoke()
                self.search_cashManagement(treeview, informations, parameters=parameters, type_search='last', save_seacrh=False)
        else:
            # show message error =====================================================
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_cashManagement(self, treeview=None, informations=None, parameters=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch[parameters['type_cash']] = searchCashManagement.format(
                parameters['typeDate'],
                parameters['table'],
                informations[0],
                informations[1],
                informations[2],
                informations[3],
                informations[4],
                informations[5],
                informations[6],
                informations[7],
                f's_{informations[12]}'.lower() if informations[11] != '' else 's_cartão',
                informations[11],
                informations[8],
                informations[9],
                '',
                parameters['typeDate'],
                informations[10],
                informations[13].replace('/', '_').lower()
            )

        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['cash'].searchDatabase(searchCashManagement.format(
                    parameters['typeDate'],
                    parameters['table'],
                    informations[0],
                    informations[1],
                    informations[2],
                    informations[3],
                    informations[4],
                    informations[5],
                    informations[6],
                    informations[7],
                    f's_{informations[12]}'.lower() if informations[11] != '' else 's_cartão',
                    informations[11],
                    informations[8],
                    informations[9],
                    '',
                    parameters['typeDate'],
                    informations[10],
                    informations[13].replace('/', '_').lower()
                ))
            case 'closeDay':
                informationsDataBase = self.dataBases['cash'].searchDatabase(searchCashManagement.format(
                    parameters['typeDate'],
                    parameters['table'],
                    informations[0],
                    informations[1],
                    informations[2],
                    informations[3],
                    informations[4],
                    informations[5],
                    informations[6],
                    informations[7],
                    f's_{informations[12]}'.lower() if informations[11] != '' else 's_cartão',
                    informations[11],
                    informations[8],
                    informations[9],
                    'DIA FINALIZADO',
                    parameters['typeDate'],
                    informations[10],
                    informations[13].replace('/', '_').lower()
                ))
            case 'last':
                informationsDataBase = self.dataBases['cash'].searchDatabase(self.lastSearch[parameters['type_cash']])
            case 'all':
                informationsDataBase = self.dataBases['cash'].searchDatabase(searchAll.format(parameters['table']))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, parameters['type_cash'])
            self.insert_treeview_informations(treeview, informationsDataBase, parameters['type_cash'])
        else:
            return informationsDataBase

    def search_cashManagementGeneral(self, treeview=None, informations=None, parameters=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch[parameters['type_cash']] = searchCashManagementGeneral.format(
                parameters['table'],
                informations[0],
                informations[1],
                informations[2],
                informations[3],
                informations[4],
                informations[5],
                informations[6],
                informations[7],
                informations[8],
                f'De {informations[9]} até {informations[10]}',
                informations[11].replace('/', '_').lower()
            )

        # pick up informations =========================================
        informationsDataBase = []
        match type_search:
            case 'new':
                informationsDataBase = self.dataBases['cash'].searchDatabase(searchCashManagementGeneral.format(
                    parameters['table'],
                    informations[0],
                    informations[1],
                    informations[2],
                    informations[3],
                    informations[4],
                    informations[5],
                    informations[6],
                    informations[7],
                    informations[8],
                    informations[9],
                    informations[11].replace('/', '_').lower()
                ))
            case 'last':
                informationsDataBase = self.dataBases['cash'].searchDatabase(self.lastSearch[parameters['type_cash']])
            case 'all':
                informationsDataBase = self.dataBases['cash'].searchDatabase(searchAll.format(parameters['table']))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, parameters['type_cash'])
            self.insert_treeview_informations(treeview, informationsDataBase, parameters['type_cash'])
        else:
            return informationsDataBase

    def update_cashManagement(self, treeview, informations, parameters):
        # update informations =========================================
        if treeview.selection():
            # pick type of date =====================
            def date(type_date):
                match type_date:
                    case 'data':
                        return datetime.today().strftime('%d/%m/%Y') if informations[10] == '' else informations[10].upper()
                    case 'mês':
                        return datetime.today().strftime('%m/%Y') if informations[9] == '' else informations[9].upper()

            if self.selection_treeview(treeview)[0][17] in ['DIA EM ANDAMENTO', 'MÊS EM ANDAMENTO', 'MÊS FINALIZADO']:
                if self.validation(informations[0:11], 5) and self.validation(informations[0:2], 7) and self.validation(informations[2:10], 8):
                    # pick value for exit =======================
                    exitValue = self.treating_numbers(informations[11] if informations[11] != '' else '0', 1)
                    value = self.dataBases['cash'].searchDatabase(f'SELECT {"s_" + informations[12].lower() if informations[12] != "" else "s_cartão"} FROM {parameters["table"]} WHERE ID = {self.selection_treeview(treeview)[0][0]}')[0][0]
                    self.dataBases['cash'].crud(
                        parameters['sqlUpdate'].format(
                            parameters['table'],
                            informations[0].upper(),
                            informations[1].upper(),
                            self.treating_numbers(informations[2], 1),
                            self.treating_numbers(informations[3], 1),
                            self.treating_numbers(informations[4], 1),
                            self.treating_numbers(informations[5], 1),
                            self.treating_numbers(informations[6], 1),
                            self.treating_numbers(informations[7], 1),
                            "s_" + informations[12].lower() if informations[12] != "" else "s_cartão",
                            self.treating_numbers(values=[value, exitValue], type_treating=4),
                            self.treating_numbers(informations[8], 1),
                            self.treating_numbers(informations[9], 1),
                            parameters['typeDate'],
                            date(parameters['typeDate']),
                            self.selection_treeview(treeview)[0][0]
                        )
                    )
                    # updating value received =====================================
                    totalReceived = self.treating_numbers(
                        values=[self.treating_numbers(informations[2], 1), self.treating_numbers(informations[3], 1), self.treating_numbers(informations[4], 1), self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1), self.treating_numbers(informations[7], 1)], type_treating=4
                    ) if parameters['table'] == 'Gerenciamento_do_dia' else informations[9]

                    discount = self.treating_numbers(values=self.dataBases['cash'].searchDatabase(f'SELECT s_cartão, s_dinheiro, s_transferência, s_nota, s_permuta FROM {parameters["table"]} WHERE ID = {self.selection_treeview(treeview)[0][0]}')[0], type_treating=4)

                    if parameters['table'] == 'Gerenciamento_do_mês':
                        if informations[10] == '':
                            discount = 'R$0,00'
                        else:
                            discount = self.treating_numbers(informations[10], 1)

                    self.dataBases['cash'].crud(f'UPDATE {parameters["table"]} SET t_recebido = "{self.treating_numbers(values=[totalReceived, discount], type_treating=5)}" WHERE ID = {self.selection_treeview(treeview)[0][0]}')
                    # delete informations of treeview ==============================
                    self.delete_informations_treeview(treeview, parameters['type_cash'])

                    # deleting and inserting informations in treeview ===============================
                    self.search_cashManagement(
                        treeview, informations, parameters=parameters, type_search='last', save_seacrh=False
                    )

                    # show message of concluded
                    self.message_window(1, 'Concluído', messagein=f'Dia atualizado com sucesso')
                else:
                    # show message error =====================================================
                    self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')
            else:
                if self.message_window(4, 'Comfimação', f'Esse item ja foi fechado, deseja alterar ele?'):
                    self.password_window(
                        self.update_cashManagementClose, {
                            'treeview': treeview,
                            'informations': informations,
                            'parameters': {
                                'sqlUpdate': parameters['sqlUpdate'],
                                'sqlSearch': searchCashManagement,
                                'table': parameters['table'],
                                'type_cash': parameters['type_cash'],
                                'typeDate': parameters['typeDate']
                            }
                        }
                    )
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')

    def update_cashManagementClose(self, treeview, informations, parameters):
        # update informations =========================================
        if treeview.selection():
            # pick type of date =====================
            def date(type_date):
                match type_date:
                    case 'data':
                        return datetime.today().strftime('%d/%m/%Y') if informations[10] == '' else informations[10].upper()
                    case 'mês':
                        return datetime.today().strftime('%m/%Y') if informations[8] == '' else informations[8].upper()

            if self.validation(informations[0:11], 5) and self.validation(informations[0:2], 7) and self.validation(informations[2:10], 8):
                # pick value for exit =======================
                exitValue = self.treating_numbers(informations[11] if informations[11] != '' else '0', 1)
                value = self.dataBases['cash'].searchDatabase(f'SELECT {"s_" + informations[12].lower() if informations[12] != "" else "s_cartão"} FROM {parameters["table"]} WHERE ID = {self.selection_treeview(treeview)[0][0]}')[0][0]
                self.dataBases['cash'].crud(
                    parameters['sqlUpdate'].format(
                        parameters['table'],
                        informations[0].upper(),
                        informations[1].upper(),
                        self.treating_numbers(informations[2], 1),
                        self.treating_numbers(informations[3], 1),
                        self.treating_numbers(informations[4], 1),
                        self.treating_numbers(informations[5], 1),
                        self.treating_numbers(informations[6], 1),
                        self.treating_numbers(informations[7], 1),
                        "s_" + informations[12].lower() if informations[12] != "" else "s_cartão",
                        self.treating_numbers(values=[value, exitValue], type_treating=4),
                        self.treating_numbers(informations[8], 1),
                        self.treating_numbers(informations[9], 1),
                        parameters['typeDate'],
                        date(parameters['typeDate']),
                        self.selection_treeview(treeview)[0][0]
                    )
                )
                # updating value received =====================================
                totalReceived = self.treating_numbers(
                    values=[self.treating_numbers(informations[2], 1), self.treating_numbers(informations[3], 1), self.treating_numbers(informations[4], 1), self.treating_numbers(informations[5], 1), self.treating_numbers(informations[6], 1), self.treating_numbers(informations[7], 1)], type_treating=4
                ) if parameters['table'] == 'Gerenciamento_do_dia' else informations[8]

                discount = self.treating_numbers(values=self.dataBases['cash'].searchDatabase(f'SELECT s_cartão, s_dinheiro, s_transferência, s_nota, s_permuta FROM {parameters["table"]} WHERE ID = {self.selection_treeview(treeview)[0][0]}')[0], type_treating=4)
                self.dataBases['cash'].crud(f'UPDATE {parameters["table"]} SET t_recebido = "{self.treating_numbers(values=[totalReceived, discount], type_treating=5)}" WHERE ID = {self.selection_treeview(treeview)[0][0]}')
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, parameters['type_cash'])

                # deleting and inserting informations in treeview ===============================
                self.search_cashManagement(
                    treeview, informations, parameters=parameters, type_search='last', save_seacrh=False
                )

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'Dia atualizado com sucesso')
            else:
                # show message error =====================================================
                self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')

    def close_cash(self, treeview, parameters, button, button2):
        # update informations =========================================
        if treeview.selection():
            if self.selection_treeview(treeview)[0][17] in ['DIA EM ANDAMENTO', 'MÊS EM ANDAMENTO']:
                if self.message_window(4, 'Comfimação', f'Você tem certeza que quer Fechar o item?'):
                    self.dataBases['cash'].crud(
                        closeDayCashManagement.format(
                            parameters['table'],
                            parameters['close'],
                            self.selection_treeview(treeview)[0][0]
                        )
                    )
                    button.invoke()
                    self.search_cashManagement(treeview, parameters=parameters, type_search='last', save_seacrh=False)
                    # show message of concluded
                    button2.invoke()
                    self.message_window(1, 'Concluído', messagein=f'Item fechado com sucesso')
            else:
                self.message_window(1, 'Concluído', messagein=f'Item já foi fechado')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')

    def delete_cashManagement(self, treeview, parameters):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'cash', parameters['table'])

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, parameters['type_cash'])

                # insert informations in treeview ===============================
                self.search_cashManagement(treeview, parameters=parameters, type_search='last', save_seacrh=False)

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Dados(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def pick_informations_for_cash(self, entrys, date=datetime.today().strftime("%d/%m/%Y"), type_informations='day'):
        match type_informations:
            case 'day':
                # deleting informations of entrys ============================================
                for entry in entrys[0:11]:
                    if isinstance(entry, CTkComboBox):
                        entry.set('')
                    else:
                        entry.delete(0, END)
                # informations of schedule and sold ===========================================
                informationsSchedule = self.dataBases['schedule'].searchDatabase(f'SELECT * FROM Agenda WHERE data LIKE "%{date if date != "" else datetime.today().strftime("%d/%m/%Y")}%"')
                informationsSold = self.dataBases['stock'].searchDatabase(f'SELECT * FROM Estoque_de_vendidos WHERE venda LIKE "%{date if date != "" else datetime.today().strftime("%d/%m/%Y")}%"')
                # treating informatios of day for entrys
                informationsOfDay = [
                    len([client for client in informationsSchedule]),
                    len([product for product in informationsSold]),
                    self.treating_numbers(
                        type_treating=4,
                        values=[
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSchedule if value[4] in ['CARTÃO', 'CARTAO']], ide=3),
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSold if value[10] in ['CARTÃO', 'CARTAO']], ide=7)
                        ]
                    ),
                    self.treating_numbers(
                        type_treating=4,
                        values=[
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSchedule if value[4] in ['DINHEIRO']], ide=3),
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSold if value[10] in ['DINHEIRO']], ide=7)
                        ]
                    ),
                    self.treating_numbers(
                        type_treating=4,
                        values=[
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSchedule if value[4] in ['TRANSFERÊNCIA', 'TRANSFERENCIA']], ide=3),
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSold if value[10] in ['TRANSFERÊNCIA', 'TRANSFERENCIA']], ide=7)
                        ]
                    ),
                    self.treating_numbers(
                        type_treating=4,
                        values=[
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSchedule if value[4] in ['NOTA', 'FIADO', 'NOTINHA']], ide=3),
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSold if value[10] in ['NOTA', 'FIADO', 'NOTINHA']], ide=7)
                        ]
                    ),
                    self.treating_numbers(
                        type_treating=4,
                        values=[
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSchedule if value[4] in ['PERMUTA', 'SEM PAGAMENTO', 'NÃO FOI PAGO']], ide=3),
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSold if value[10] in ['PERMUTA', 'SEM PAGAMENTO', 'NÃO FOI PAGO']], ide=7)
                        ]
                    ),
                    self.treating_numbers(
                        type_treating=4,
                        values=[
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSchedule if value[4] in ['VALE', 'vale']], ide=3),
                            self.treating_numbers(type_treating=2, values=[value for value in informationsSold if value[10] in ['VALE', 'vale']], ide=7)
                        ]
                    ),
                ]
                # inserting informations of day ====================================
                for index, information in enumerate(informationsOfDay):
                    if entrys[index] != self.CashDayEntry:
                        entrys[index].insert(0, information)
                entrys[9].insert(0, self.treating_numbers(type_treating=4, values=informationsOfDay[2:8]))
                entrys[10].insert(0, date if date != '' else datetime.today().strftime("%d/%m/%Y"))
                # searching schedules and products ===================================
                self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', '', entrys[10].get(), ''], type_search='resumeForCash', save_seacrh=False)
                self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', '', entrys[10].get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')
            case 'month':
                # deleting informations of entrys ============================================
                for entry in entrys[0:11]:
                    if isinstance(entry, CTkComboBox):
                        entry.set('')
                    else:
                        entry.delete(0, END)
                # informations of schedule and sold ===========================================
                informationsDay = self.dataBases['cash'].searchDatabase(f'SELECT * FROM Gerenciamento_do_dia WHERE data LIKE "%{date if date != "" else datetime.today().strftime("%m/%Y")}%" AND status LIKE "%DIA FINALIZADO%"')
                # treating informatios of day for entrys =====================================
                informationsOfMonth = [
                    self.treating_numbers(
                        type_treating=6,
                        values=[value[1] for value in informationsDay],
                    ),
                    self.treating_numbers(
                        type_treating=6,
                        values=[value[2] for value in informationsDay]
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=3
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=4
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=5
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=6
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=7
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=8
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=14
                    ),
                    self.treating_numbers(
                        type_treating=2,
                        values=informationsDay,
                        ide=15
                    ),
                ]
                print(informationsOfMonth)
                # inserting informations of day ====================================
                for index, information in enumerate(informationsOfMonth):
                    entrys[index].insert(0, information)
                entrys[10].insert(0, date if date != "" else datetime.today().strftime("%m/%Y"))
                # searching days ===================================
                self.search_cashManagement(
                    self.treeviewCashMonthDay,
                    ['', '', '', '', '', '', '', '', '', '', date if date != "" else datetime.today().strftime("%m/%Y"), '', '', 'data'],
                    parameters={
                        'typeDate': 'data',
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay'
                    },
                    save_seacrh=False,
                    type_search='closeDay'
                )

    def pick_informations_for_cashGeneral(self, entrys):
        # deleting informations of entrys ============================================
        for entry in entrys[0:9]:
            if isinstance(entry, CTkComboBox):
                entry.set('')
            else:
                entry.delete(0, END)

        informationsOfDays = self.calculateDate([entrys[9].get(), entrys[10].get()])

        # inserting informations of day ====================================
        for index, information in enumerate(informationsOfDays[0:7]):
            entrys[index].insert(0, information)
        entrys[7].insert(0, informationsOfDays[12])
        entrys[8].insert(0, informationsOfDays[13])

    def pick_infromations_of_schedule_and_products(self, date):
        # searching schedules and products ===================================
        self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', '', date.get(), ''], type_search='resumeForCash', save_seacrh=False)
        self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', '', date.get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')

    def create_pdf_cashManagement(self, treeview, parameters, type_pdf='normal'):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # informations ============================================
            for information in informationsTreeview:
                parameters['tablePart1'].append(information[0:8])
            for information in informationsTreeview:
                parameters['tablePart2'].append(information[8:16] if type_pdf == 'normal' else information[8:15])

            if type_pdf == 'normal':
                parameters['tablePart2'][1].append(parameters['typeDate'])
                parameters['supplementaryTable'][1].insert(0, parameters['type_message'])
                parameters['supplementaryTable'].append(self.informations_supplementarys_cashManagement(informationsTreeview, parameters['type_message'])[1:])
            else:
                parameters['supplementaryTable'].append(self.informations_supplementarys_cashManagement(informationsTreeview)[1:])

            # create tables ===========================================
            table1 = Table(parameters['tablePart1'])
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(parameters['tablePart2'])
            table2.setStyle(TableStyle(styleTableInformationsTreeview))
            table3 = Table(parameters['supplementaryTable'])
            table3.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del parameters['tablePart1'][2:]
            del parameters['tablePart2'][2:]
            del parameters['supplementaryTable'][2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2, table3])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_cashManagement(self, treeview, parameters, type_msn='noemal'):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            if type_msn == 'normal':
                # show menssege ================================================
                self.message_window(
                    1,
                    'Informações sobre a tabela',
                    messageCashManagement.format(*self.informations_supplementarys_cashManagement(informationsTreeview, parameters['type_message']))
                )
            else:
                self.message_window(
                    1,
                    'Informações sobre a tabela',
                    messageCashManagementGeneral.format(*self.informations_supplementarys_cashManagement(informationsTreeview)[1:])
                )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def informations_supplementarys_cashManagement(self, informations, type_date=None):
        # píck up informations supplementarys ==============================
        totalClients = self.treating_numbers(values=[client[1] for client in informations], type_treating=6)
        totalProducts = self.treating_numbers(values=[client[2] for client in informations], type_treating=6)
        totalReceived = self.treating_numbers(values=[client[14] for client in informations], type_treating=4)
        totalExit = []
        for information in informations:
            totalExit.append(self.treating_numbers(values=[information[8], information[9], information[10], information[11], information[12]], type_treating=4))
        totalExit = self.treating_numbers(values=totalExit, type_treating=4)
        if type_date is not None:
            return [type_date, len(informations), totalClients, totalProducts, totalReceived, totalExit]
        else:
            return [len(informations), totalClients, totalProducts, totalReceived, totalExit]

    def search_informations_of_cash(self, treeview, type_search):
        if len(self.pick_informations_treeview(treeview)) > 0:
            dateForSearch = self.selection_treeview(treeview)[0][16]
            match type_search:
                case 'day':
                    # searching schedules and products ===================================
                    self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', '', dateForSearch, ''], type_search='resumeForCash', save_seacrh=False)
                    self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', '', dateForSearch], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')
                case 'month':
                    # searching days ===================================
                    self.search_cashManagement(
                        self.treeviewCashMonthDay,
                        ['', '', '', '', '', '', '', '', '', dateForSearch if dateForSearch != "" else datetime.today().strftime("%m/%Y"), '', '', 'data'],
                        parameters={
                            'typeDate': 'data',
                            'table': 'Gerenciamento_do_dia',
                            'type_cash': 'cashDay'
                        },
                        save_seacrh=False,
                        type_search='closeDay'
                    )


class FunctionsOfPayment(GeneralFunctions):

    def register_payment(self, informations, treeview):
        inoivicing = self.treating_numbers(informations[3], 1)
        payment = self.treating_numbers(informations[5], 1)
        if self.validation(informations[0:6], 5) and self.validation([informations[2], informations[4]], 7) and self.validation([inoivicing, payment], 8):
            if self.message_window(4, 'Comfimação', f'Finalisar o pagamento de {informations[0].title()}?'):
                # informations of treeview ====================
                self.dataBases['cash'].crud(
                    registerCashPayment.format(
                        informations[0].upper(), informations[1].upper(), informations[2].upper(), self.treating_numbers(informations[3], 1), informations[4].upper(), self.treating_numbers(informations[5], 1),
                        informations[6].upper(), datetime.today().strftime("%d/%m/%Y"), informations[7].upper()
                    )
                )
                # deleting and inserting informations in treeview ===============================
                self.search_payment(treeview, informations, 'all', save_seacrh=False)
        else:
            # show message error =====================================================
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_payment(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['cashPayment'] = searchCashPayment.format(
                informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(),
                informations[6].upper(), informations[7].upper(), informations[8].replace(' ', '_').replace('/', '_')
            )
        # pick up informations =========================================
        informationsDatabase = []
        match type_search:
            case 'new':
                informationsDatabase = self.dataBases['cash'].searchDatabase(
                    searchCashPayment.format(
                        informations[0].upper(), informations[1].upper(), informations[2].upper(), informations[3].upper(), informations[4].upper(), informations[5].upper(),
                        informations[6].upper(), informations[7].upper(), informations[8].replace(' ', '_').replace('/', '_')
                    )
                )
            case 'last':
                informationsDatabase = self.dataBases['cash'].searchDatabase(self.lastSearch['cashPayment'])
            case 'all':
                informationsDatabase = self.dataBases['cash'].searchDatabase(searchAll.format('Gerenciador_de_pagamentos'))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'cashPayment')
            self.insert_treeview_informations(treeview, informationsDatabase, 'cashPayment')
        else:
            return informationsDatabase

    def update_payment(self, treeview, informations):
        if self.validation([informations[2], informations[4]], 7) and self.validation([informations[3], informations[5]], 8):
            # update informations =========================================
            if treeview.selection():
                informationsDataBase = self.dataBases['cash'].crud(
                    updateCashPayment.format(
                        informations[0].upper(), informations[1].upper(), informations[2].upper(), self.treating_numbers(informations[3], 1), informations[4].upper(), self.treating_numbers(informations[5], 1),
                        informations[6].upper(), informations[7].upper(), self.selection_treeview(treeview)[0][0]
                    )
                )
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'cashPayment')

                # insert informations in treeview ===============================
                self.search_payment(treeview, informations, 'last', save_seacrh=False)

                # refresh =======================================================
                self.refresh_combobox_client()

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'Pagamento de {informations[0].title()} atualizado com sucesso')
            else:
                self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')
        else:
            # show message error =====================================================
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def delete_payment(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'cash', 'Gerenciador_de_pagamentos')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'cashPayment')

                # insert informations in treeview ===============================
                self.search_payment(treeview, type_search='last', save_seacrh=False)

                # refresh =======================================================
                self.refresh_combobox_client()

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Pagamentos(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def create_pdf_payment(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # Collecting informations for messege===============================
            informationsComplementary = [
                len(informationsTreeview),
                self.treating_numbers(values=[row[3] for row in informationsTreeview], type_treating=6),
                self.treating_numbers(values=[row[4] for row in informationsTreeview], type_treating=4),
            ]

            # informations ============================================
            for information in informationsTreeview:
                tableWithInformationsCashPaymentTreeview1.append(information[0:5])
            for information in informationsTreeview:
                tableWithInformationsCashPaymentTreeview2.append(information[5:9])
            tableWithInformationsComplementaryCashPayment.append(informationsComplementary)

            # create tables ===========================================
            table1 = Table(tableWithInformationsCashPaymentTreeview1)
            table1.setStyle(TableStyle(styleTableInformationsTreeview))
            table2 = Table(tableWithInformationsCashPaymentTreeview2)
            table2.setStyle(TableStyle(styleTableInformationsTreeview))
            table3 = Table(tableWithInformationsComplementaryCashPayment)
            table3.setStyle(TableStyle(styleTableInformationsComplementary))

            # reseting tables =========================================
            del tableWithInformationsCashPaymentTreeview1[2:]
            del tableWithInformationsCashPaymentTreeview2[2:]
            del tableWithInformationsComplementaryCashPayment[2:]

            # creating pdf ============================================
            saveDirectory = self.create_pdf(treeview, [table1, table2, table3])
            if saveDirectory is not None:
                self.message_window(1, 'Concluído', messagein=f'O arquivo foi salvo em "{saveDirectory}"')
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def message_informations_payment(self, treeview):
        if informationsTreeview := self.pick_informations_treeview(treeview):
            # shoe menssege ================================================
            self.message_window(
                1,
                'Informações sobre a tabela',
                f'Total de Pagamentos = {len(informationsTreeview)}\n'
                f'Total de clientes = {self.treating_numbers(values=[row[3] for row in informationsTreeview], type_treating=6)}\n'
                f'Total faturado = {self.treating_numbers(values=[row[4] for row in informationsTreeview], type_treating=4)}\n'
            )
        else:
            self.message_window(2, 'Sem registro', 'A tabela esta vazia')

    def pick_informations_for_payment(self, entrys, data, professional='', method_pay=''):
        # searching information of schedule =========================
        data.append(professional)
        data.append(method_pay)
        # treating information ===================================
        informationsPayment = self.calculateDate(data, 'payment')
        # inserting informations in entrys ======================
        for entry in entrys[1:7]:
            entry.delete(0, END)
        entrys[1].insert(0, data[0])
        entrys[2].insert(0, data[1])
        entrys[3].insert(0, informationsPayment[0])
        entrys[4].insert(0, informationsPayment[1])


class FunctionsOfLogin(GeneralFunctions):

    def register_users(self, treeview, informations):
        if self.validation(informations, 5):
            if self.message_window(4, 'Comfimação', f'Finalisar o cadastro de {informations[0].title()}?'):
                # informations of treeview ====================
                self.dataBases['informations'].crud(
                    registerUsers.format(
                        informations[0], self.criptography.crypt(informations[1], type_cryptography="hash"),
                        'NORMAL' if informations[2] == '' else informations[2]
                    )
                )
                # deleting and inserting informations in treeview ===============================
                self.search_users(treeview, informations, 'all', save_seacrh=False)
        else:
            # show message error =====================================================
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def search_users(self, treeview=None, informations=None, type_search='new', save_seacrh=True, insert=True):
        # save last search ============================================
        if save_seacrh:
            self.lastSearch['users'] = searchUsers.format(
                informations[0].upper(), informations[2].upper()
            )

        # pick up informations =========================================
        informationsDatabase = []
        match type_search:
            case 'new':
                informationsDatabase = self.dataBases['informations'].searchDatabase(
                    searchUsers.format(
                        informations[0].upper(), informations[2].upper()
                    )
                )
            case 'last':
                informationsDatabase = self.dataBases['informations'].searchDatabase(self.lastSearch['users'])
            case 'all':
                informationsDatabase = self.dataBases['informations'].searchDatabase(searchAll.format('Usuários'))

        if insert:
            # deleting and inserting informations in treeview ===============================
            self.delete_informations_treeview(treeview, 'users')
            self.insert_treeview_informations(treeview, informationsDatabase, 'users')
        else:
            return informationsDatabase

    def update_users(self, treeview, informations):
        if self.validation([informations[0], informations[2]], 5):
            # update informations =========================================
            if treeview.selection():
                informationsDataBase = self.dataBases['informations'].crud(
                    updateUsers.format(
                        informations[0], self.criptography.crypt(informations[1], type_cryptography="hash"), informations[2].upper(),
                        self.selection_treeview(treeview)[0][0]
                    )
                )
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'users')

                # insert informations in treeview ===============================
                self.search_users(treeview, informations, 'last', save_seacrh=False)

                # show message of concluded
                self.message_window(1, 'Concluído', messagein=f'Usuário {informations[0].title()} atualizado com sucesso')
            else:
                self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para atualizar')
        else:
            # show message error =====================================================
            self.message_window(3, 'Erro', 'Verifique se os campos estão preenchidos ou corretos')

    def delete_users(self, treeview):
        if treeview.selection():
            # deleting inforations =======================================
            delete = self.delete_information(treeview, 'informations', 'Usuários')

            if delete:
                # delete informations of treeview ==============================
                self.delete_informations_treeview(treeview, 'users')

                # insert informations in treeview ===============================
                self.search_users(treeview, type_search='last', save_seacrh=False)

                # shoe message of concluded
                self.message_window(1, 'Concluído', messagein=f'Pagamentos(s) deletado(s) com sucesso')
        else:
            self.message_window(3, 'Sem seleção', 'Selecione algum item na lista para deletar')

    def password_window(self, function, parameter):
        self.passwordWindow = Toplevel()
        self.passwordWindow.title('Senha de administrador - Studio Rosa')
        width = self.passwordWindow.winfo_screenwidth()
        height = self.passwordWindow.winfo_screenheight()
        posx = width / 2 - 340 / 2
        posy = height / 2 - 270 / 2
        self.passwordWindow.geometry('340x270+%d+%d' % (posx, posy))
        self.passwordWindow.maxsize(340, 270)
        self.passwordWindow.config(bg='#FFFFFF')
        self.passwordWindow.focus_force()
        self.passwordWindow.iconphoto(False, PhotoImage(file='assets/Mascara-Studio.png'))

        # frame of inputs ===========================================================
        frameInputs = self.frame(self.passwordWindow, 0, 0.01, 1, 0.985)

        # photo ---------------------------------------
        self.labelPadlock = self.labels(self.passwordWindow, '', 0.3, 0.1, width=0.4, height=0.2, photo=self.image('assets/icon_password.png', (56, 56))[0], position=CENTER)

        # password ------------------------------------
        password = self.entry(frameInputs, 0.1, 0.35, 0.8, 0.16, type_entry='entry', show='*')
        password.focus_force()

        # visibility ---------------------------------
        visibilityPasswordBtn = self.button(
            self.passwordWindow, '', 0.76, 0.38, 0.13, 0.1, photo=self.image('assets/icon_eyeClose.png', (26, 26))[0],
            type_btn='buttonPhoto', hover_cursor='white', function=lambda: self.toggle_visibility(password, visibilityPasswordBtn)
        )
        password.bind('<KeyPress>', lambda e: [password.configure(fg_color='#FFFFFF'), visibilityPasswordBtn.configure(fg_color='#FFFFFF')])
        password.bind('<Return>', lambda e: self.validating_user([password, visibilityPasswordBtn], function, 'password', parameters=parameter, window_password=self.passwordWindow))

        # comfirm -------------
        comfirmBtn = self.button(
            self.passwordWindow, 'Confirmar', 0.1, 0.56, 0.8, 0.17,
            function=lambda: self.validating_user([password, visibilityPasswordBtn], function, 'password', parameters=parameter, window_password=self.passwordWindow)
        )

        # cancel -------------
        cancelBtn = self.button(self.passwordWindow, 'Cancelar', 0.1, 0.76, 0.8, 0.17, function=lambda: self.passwordWindow.destroy())

    def validating_user(self, entrys, function, type_password, parameters, window_password=None):
        # searching infomation of user =========================
        informations = []
        match type_password:
            case 'login':
                informations = self.dataBases['informations'].searchDatabase(
                    f'SELECT * FROM Usuários WHERE nome = "{entrys[0].get()}" AND senha = "{self.criptography.crypt(entrys[1].get(), type_cryptography="hash")}"'
                )
            case 'password':
                informations = self.dataBases['informations'].searchDatabase(
                    f'SELECT * FROM Usuários WHERE senha = "{self.criptography.crypt(entrys[0].get(), type_cryptography="hash")}" AND nivel = "ADMINISTRADOR"'
                )

        if informations:
            if type_password == 'password':
                window_password.destroy()
            return function(*parameters.values()) if isinstance(parameters, dict) else function(*parameters.values())
        else:
            colors = ['#f07f7f', '#FFFFFF']
            if len(entrys) > 2:
                entrys[0].configure(fg_color='#f07f7f')
                entrys[1].configure(fg_color='#f07f7f')
                entrys[2].configure(fg_color='#f07f7f')
            else:
                entrys[0].configure(fg_color='#f07f7f')
                entrys[1].configure(fg_color='#f07f7f')

    def save_user(self, user):
        self.user = user
    def toggle_visibility(self, entry, button):
        current_show = entry.cget("show")
        if current_show == "*":
            entry.configure(show="")
            button.configure(image=self.image('assets/icon_eyeOpen.png', (26, 26))[0])
        else:
            entry.configure(show="*")
            button.configure(image=self.image('assets/icon_eyeClose.png', (26, 26))[0])

    def open_software(self, event):
        self.loginWindow.withdraw()
        self.main_window()
