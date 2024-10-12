# libs of python ==========
from tkinter import ttk
from tkcalendar import DateEntry

# my modules ==============
from databaseConnection import DataBase, Criptography
from functions import *
from interface import Interface


class Aplication(
    Interface,
    FunctionsOfSchedule,
    FunctionsOfCustomsInformations,
    FunctionsOfProfessionalInformations,
    FunctionsOfServiceInformations,
    # FunctionsOfBarCodeInformations,
    FunctionsOfInformationsStock,
    FunctionsOfStockInformations,
    FunctionsOfCashManagement,
    FunctionsOfPayment,
    FunctionsOfLogin
):

    def __init__(self):
        self.lineTreeviewColor = {}
        self.lastSearch = {}
        self.dataBases = {
            'schedule': DataBase('resources/Agendamentos.db'),
            'informations': DataBase('resources/Informações.db'),
            'stock': DataBase('resources/Estoque.db'),
            'cash': DataBase('resources/Caixa.db'),
            'config': DataBase('resources/config.db'),
            'backup': DataBase('backup.db')
        }
        self.criptography = Criptography()
        self.acess = False
        super().__init__()
        self.login_window()

    def login_window(self):
        self.loginWindow = Tk()
        self.loginWindow.title('Login - StudioPro')
        width = self.loginWindow.winfo_screenwidth()
        height = self.loginWindow.winfo_screenheight()
        posx = width / 2 - 700 / 2
        posy = height / 2 - 400 / 2
        self.loginWindow.geometry('700x400+%d+%d' % (posx, posy))
        self.loginWindow.config(bg='#FFFFFF')
        self.loginWindow.iconphoto(False, PhotoImage(file='assets/Mascara-Studio.png'))

        # logo image ==============================
        logoImage = self.labels(self.loginWindow, '', 0.009, 0.01, width=0.48, height=0.98, photo=self.image('assets/Mascara-Studio.png', (256, 210))[0], position=CENTER)

        # frame of inputs =========================
        frameInputs = self.frame(self.loginWindow, 0.5, 0.005, 0.49, 0.985, border=2, radius=10)

        # name login ---------------------------
        labelLogin = self.labels(
            frameInputs, 'LOGIN', 0.253, 0.05, width=0.5, height=0.2, position=CENTER, size=50, color='#171717',
            font='Handmade'
        )

        # user name and password -----------------------------
        userName = self.entry(
            frameInputs, 0.1, 0.3, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Usuário'
        )
        userName.bind('<FocusIn>', lambda e: userName.configure(fg_color='#FFFFFF'))

        password = self.entry(
            frameInputs, 0.1, 0.5, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Senha', show='*'
        )

        # visibility ---------------------------------
        visibilityPasswordBtn = self.button(
            frameInputs, '', 0.76, 0.52, 0.13, 0.08, photo=self.image('assets/icon_eyeClose.png', (26, 26))[0],
            type_btn='buttonPhoto', background='white', hover_cursor='white', function=lambda: self.toggle_visibility(password, visibilityPasswordBtn)
        )
        password.bind('<FocusIn>', lambda e: [password.configure(fg_color='#FFFFFF'), visibilityPasswordBtn.configure(fg_color='#FFFFFF')])
        password.bind('<Return>', lambda e: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''}))

        # line separator higher --------------------
        lineHigher = Canvas(frameInputs, background='#FFFFFF', highlightthickness=0)
        lineHigher.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.1)
        lineHigher.create_line(1, 15, 1000, 15, fill='#171717', width=2)

        # button of login and button of register ----------------------
        loginBtn = self.button(
            frameInputs, 'Iniciar sessão', 0.1, 0.72, 0.8, 0.1, background='#f25298',
            border=0, color='black',
            function=lambda: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''})
        )
        closeBtn = self.button(
            frameInputs, 'Fechar', 0.1, 0.85, 0.8, 0.1, background='black',
            border=0, color='#f25298', function=lambda: self.loginWindow.destroy()
        )
        self.loginWindow.mainloop()

    # ================================== main window configure =======================================
    def main_window(self):
        # screen configure ===================================
        self.root = Toplevel()
        self.root.title('StudioPro')
        self.root.state('zoomed')
        self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}')
        self.root.configure(background='#FFFFFF')
        self.root.iconphoto(False, PhotoImage(file='assets/Mascara-Studio.png'))
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: [self.backup_dataBase_cloud(), self.backup_dataBase_local(), self.loginWindow.destroy()])
        # event bind ============================================
        self.root.bind_all('<Control-d>', lambda e: self.select_diretory_of_cloud())
        self.root.bind_all('<Control-b>', lambda e: [self.backup_dataBase_cloud(), self.backup_dataBase_local()])
        self.root.bind_all('<Control-l>', lambda e: self.loading_database_cloud())

        # style notebook
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 13, "bold"), foreground='#94315c')

        # style treeviews ==================================================
        style_treeview = ttk.Style()
        style_treeview.theme_use('vista')
        style_treeview.configure('Treeview', rowheight=27, fieldbackground='#261c20', foreground='black', font='Arial 10 bold')
        self.photosAndIcons = {
            'pdf': self.image('assets/icon_pdf.png', (46, 46)),
            'informações': self.image('assets/icon_informacoes.png', (46, 46)),
            'random': self.image('assets/icon_random.png', (36, 36)),
            'image': self.image('assets/icon_imagem.png', (26, 26)),
            'costumer': self.image('assets/icon_no_picture.png', (76, 76)),
            'employee': self.image('assets/icon_no_picture.png', (76, 76)),
            'productUse': self.image('assets/icon_product.png', (76, 76)),
            'productSale': self.image('assets/icon_product.png', (76, 76)),
            'productUseUnusable': self.image('assets/icon_product.png', (76, 76)),
            'productSaleSold': self.image('assets/icon_product.png', (76, 76)),
            'barCode': self.image('assets/icon_barCode.png', (76, 76)),
        }
        self.mainTabview = ttk.Notebook(self.root)
        self.mainTabview.place(relx=0, rely=0.01, relwidth=1, relheight=1)

        # cash register ============================================================
        self.mainCashRegisterFrame = self.main_frame_notebook(self.mainTabview, ' Caixa ')
        self.cashManagementTabview = self.notebook(self.mainCashRegisterFrame)
        # schedule management ---------------------------------------------------
        self.scheduleFrame = self.main_frame_notebook(self.cashManagementTabview, ' Cadastro de atendimento  ')
        self.frame_schedule()
        # cash management ---------------------------------------------------
        self.cashFrame = self.main_frame_notebook(self.cashManagementTabview, ' Gerenciamento de caixa ')
        self.typeCashManagement = self.tabvieew(self.cashFrame, 0, 0, 1, 0.98, background='white', border='white')
        # day finish
        self.typeCashManagement.add(' Gerenciamento do dia ')
        self.frame_cash_register_management_day()
        # month finish
        self.typeCashManagement.add(' Gerenciamento do mês ')
        self.frame_cash_register_management_month()
        # general finish
        self.typeCashManagement.add(' Gerenciamento geral ')
        self.frame_cash_register_management_general()
        # employee management ---------------------------------------------------
        self.employersPayFrame = self.main_frame_notebook(self.cashManagementTabview, ' Gerenciar pagamentos ')
        self.frame_pay_management()

        # information ============================================================
        self.mainInformationFrame = self.main_frame_notebook(self.mainTabview, ' Cadastro & Informações ')
        self.informationsManagementTabview = self.notebook(self.mainInformationFrame)
        # costumers management ---------------------------------------------------
        self.costumersFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Clientes ')
        self.frame_customers()
        # employers management ---------------------------------------------------
        self.employersFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Profissionais ')
        self.frame_employers()
        # services management ---------------------------------------------------
        self.servicesFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Serviços ')
        self.frame_service()
        # bar code management ---------------------------------------------------
        # self.barCodeFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Código de barras ')
        # self.frame_barCode()
        # stock informations -----------------------------------------------------
        self.stockInformationsFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Informações de estoque ')
        self.typeStockInformations = self.tabvieew(self.stockInformationsFrame, 0, 0, 1, 0.98, background='white', border='white')
        self.frame_stock_informations()
        # bar code management ---------------------------------------------------
        self.userFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Usuários ')
        self.frame_users()

        # stock ============================================================
        self.mainStockFrame = self.main_frame_notebook(self.mainTabview, ' Estoque ')
        self.inventoryControlManagementTabview = self.notebook(self.mainStockFrame)
        # stock management ---------------------------------------------------
        self.inventoryControlFrame = self.main_frame_notebook(self.inventoryControlManagementTabview, ' Gerenciamento de estoque ')
        self.typeStockmanagement = self.tabvieew(self.inventoryControlFrame, 0, 0, 1, 0.98)
        # use stock management
        self.typeStockmanagement.add(' Estoque de uso ')
        self.frame_use_inventory_control()
        # sale stock management
        self.typeStockmanagement.add(' Estoque de venda ')
        self.frame_sale_inventory_control()
        # stock unusable management ---------------------------------------------------
        self.inventoryControlUnusableFrame = self.main_frame_notebook(self.inventoryControlManagementTabview, ' Estoque inutilizável ')
        self.typeStockUnusableManagement = self.tabvieew(self.inventoryControlUnusableFrame, 0, 0, 1, 0.98, background='#4d172e')
        # use stock management
        self.typeStockUnusableManagement.add(' Estoque de usados ')
        self.frame_use_inventory_control_unusable()
        # sale stock management
        self.typeStockUnusableManagement.add(' Estoque de vendidos ')
        self.frame_sale_inventory_control_unusable()

        # filling in lists -----------------------------------------
        self.refresh_combobox_client()
        self.refresh_combobox_professional()
        self.refresh_combobox_service()
        # self.refresh_combobox_barCode()
        self.refresh_combobox_InformationsStock()

        # keeping window ===========================================
        self.root.mainloop()

    # =================================  schedule configuration  ======================================
    def frame_schedule(self):
        # frame inputs ==========================================
        self.frameInputsSchedule = self.frame(self.scheduleFrame, 0.005, 0.01, 0.989, 0.43)

        # custom -------------
        labelCustom = self.labels(self.frameInputsSchedule, 'Cliente:', 0.02, 0.08, width=0.08)
        self.customScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.08, 0.2, 0.12, type_entry='list')

        # service -------------
        labelService = self.labels(self.frameInputsSchedule, 'Serviço:', 0.02, 0.22, width=0.15)
        self.serviceScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.12, 0.22, 0.20, 0.12, type_entry='list',
            function=lambda e: [
                self.valueScheduleEntry.delete(0, END),
                self.valueScheduleEntry.insert(
                    0,
                    [name[2] for name in self.search_service(informations=self.searching_list(self.serviceScheduleEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)][0])
                if len([name[2] for name in self.search_service(informations=self.searching_list(self.serviceScheduleEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)]) > 0 and self.serviceScheduleEntry.get() != '' else ''
            ]
        )

        # value -------------
        labelValue = self.labels(self.frameInputsSchedule, 'Valor:', 0.02, 0.36, width=0.15)
        self.valueScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.36, 0.2, 0.12, type_entry='entry')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsSchedule, 'M/Pagamento:', 0.02, 0.50, width=0.15)
        self.methodPayScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.155, 0.50, 0.165, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'PERMUTA']
        )

        # professional -------------
        labelProfessional = self.labels(self.frameInputsSchedule, 'Profissional:', 0.02, 0.64, width=0.15)
        self.professionalScheduleEntry = self.entry(self.frameInputsSchedule, 0.122, 0.64, 0.199, 0.12, type_entry='list')

        # date -------------
        labelDate = self.labels(self.frameInputsSchedule, 'Data:', 0.02, 0.78, width=0.16)
        self.dateScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.78, 0.159, 0.12, type_entry='date')
        self.dateScheduleEntry.insert(0, datetime.today().strftime('%d/%m/%Y'))

        # time -----------------
        labelTime = self.labels(self.frameInputsSchedule, 'Horário:', 0.34, 0.08, width=0.16)
        self.timeScheduleEntry = self.entry(self.frameInputsSchedule, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # marking ----------
        labelMarking = self.labels(self.frameInputsSchedule, 'Agendamento:', 0.34, 0.22, width=0.12, color='#803356')
        self.markingScheduleEntry = self.entry(self.frameInputsSchedule, 0.46, 0.22, 0.179, 0.12, type_entry='entry')

        # event bind frameInput ==========================================
        self.serviceScheduleEntry.bind("<FocusOut>", lambda e: [
            self.valueScheduleEntry.delete(0, END),
            self.valueScheduleEntry.insert(
                0,
                [name[2] for name in self.search_service(informations=self.searching_list(self.serviceScheduleEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)][0])
            if len([name[2] for name in self.search_service(informations=self.searching_list(self.serviceScheduleEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)]) > 0 and self.serviceScheduleEntry.get() != '' else ''
        ])
        self.customScheduleEntry.bind('<KeyPress>', lambda e: self.customScheduleEntry.configure(
            values=[name[1] for name in self.search_client(informations=self.searching_list(self.customScheduleEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))
        self.serviceScheduleEntry.bind('<KeyPress>', lambda e: self.serviceScheduleEntry.configure(
            values=[name[1] for name in self.search_service(informations=self.searching_list(self.serviceScheduleEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)]
        ))
        self.professionalScheduleEntry.bind('<KeyPress>', lambda e: self.professionalScheduleEntry.configure(
            values=[name[1] for name in self.search_professional(informations=self.searching_list(self.professionalScheduleEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))
        self.dateScheduleEntry.bind('<<DateEntrySelected>>', lambda e: self.search_schedule(self.treeviewSchedule, entryPicker()[0]))

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSchedule, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewSchedule, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewSchedule = self.frame(self.scheduleFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Cliente', 'Serviço', 'Valor', 'Método de Pagamento', 'Profissional',  'Data', 'Horário', 'Agendamento', 'Data de Pagamento')
        self.treeviewSchedule = self.treeview(self.frameTreeviewSchedule, informationOfTable)
        self.lineTreeviewColor['schedule'] = 0
        # event bind treeview ==========================================
        self.treeviewSchedule.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewSchedule))

        # save last search schedule ===================================
        self.lastSearch['schedule'] = ''

        # buttons management ===========================================
        functions = {
            'register': lambda: self.register_schedule(entryPicker()[0], self.treeviewSchedule),
            'search': lambda: self.search_schedule(self.treeviewSchedule, entryPicker()[0]),
            'order': lambda e: self.search_schedule(self.treeviewSchedule, entryPicker()[0]),
            'update': lambda: self.password_window(self.update_schedule, {'treeview': self.treeviewSchedule, "informations": entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_schedule, {'treeview': self.treeviewSchedule}),
            'pdf': lambda: self.create_pdf_schedule(self.treeviewSchedule),
            'informations': lambda: self.message_informations_schedule(self.treeviewSchedule)
        }
        self.orderBtnSchedule = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSchedule, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ===========================
        def entryPicker():
            entrysGet = []
            entrys = []
            for widget in self.frameInputsSchedule.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            entrysGet.append(self.orderBtnSchedule.get())
            return [entrysGet, entrys, ['', '', '', '', '', self.dateScheduleEntry.get(), '', '', self.orderBtnSchedule.get()]]

        # init search for day ===============================================
        self.search_schedule(self.treeviewSchedule, entryPicker()[0])

    '''def frame_scheduling(self):
        # frame inputs ==========================================
        self.frameInputsScheduling = self.frame(self.schedulingFrame, 0.005, 0.01, 0.989, 0.43)

        # custom ----------
        labelCustom = self.labels(self.frameInputsScheduling, 'Cliente:', 0.014, 0.13, width=0.11)
        self.customSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.125, 0.17, 0.12, type_entry='list')

        # service --------------
        labelService = self.labels(self.frameInputsScheduling, 'Serviço:', 0.014, 0.33, width=0.08)
        self.serviceSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.325, 0.17, 0.12, type_entry='list')

        # professional ---------------
        labelProfessional = self.labels(self.frameInputsScheduling, 'Profissional:', 0.014, 0.53, width=0.1)
        self.professionalSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.525, 0.17, 0.12, type_entry='list')

        # value ----------
        labelValue = self.labels(self.frameInputsScheduling, 'Valor:', 0.014, 0.73, width=0.11)
        self.valueSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.725, 0.17, 0.12, type_entry='entry')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsScheduling, 'M/Pagamento:', 0.35, 0.13, width=0.15)
        self.methodPaySchedulingEntry = self.entry(
            self.frameInputsScheduling, 0.47, 0.125, 0.17, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # date ----------
        labelDate = self.labels(self.frameInputsScheduling, 'Data:', 0.35, 0.33, width=0.1)
        self.datelSchedulingEntry = self.entry(self.frameInputsScheduling, 0.47, 0.325, 0.15, 0.12, type_entry='date', validity='yes')

        # time ----------
        labelTime = self.labels(self.frameInputsScheduling, 'Horário:', 0.35, 0.53, width=0.11)
        self.timeSchedulingEntry = self.entry(self.frameInputsScheduling, 0.47, 0.525, 0.17, 0.12, type_entry='entry')

        # cheat ----------
        labelCheat = self.labels(self.frameInputsScheduling, 'Código:', 0.35, 0.73, width=0.13, color='#803356')
        self.cheatSchedulingEntry = self.entry(self.frameInputsScheduling, 0.47, 0.725, 0.17, 0.12, type_entry='list')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsScheduling, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewScheduling, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        self.cheatSchedulingEntry.bind('<Return>', lambda e: self.register_scheduling(entryPicker()[0], type_function='add', treeview=self.treeviewScheduling, type_insert='codeEventBind', entrys=entryPicker()[1][1:4], verification=False))
        self.customSchedulingEntry.bind('<KeyPress>', lambda e: self.customSchedulingEntry.configure(
            values=[name[1] for name in self.search_client(informations=self.searching_list(self.customSchedulingEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))
        self.serviceSchedulingEntry.bind('<KeyPress>', lambda e: self.serviceSchedulingEntry.configure(
            values=[name[1] for name in self.search_service(informations=self.searching_list(self.serviceSchedulingEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)]
        ))
        self.professionalSchedulingEntry.bind('<KeyPress>', lambda e: self.professionalSchedulingEntry.configure(
            values=[name[1] for name in self.search_professional(informations=self.searching_list(self.professionalSchedulingEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))
        self.cheatSchedulingEntry.bind('<KeyPress>', lambda e: self.cheatSchedulingEntry.configure(
            values=[name[3] for name in self.search_barCode(informations=['', '', self.cheatSchedulingEntry.get(), '', 'código'], save_seacrh=False, insert=False)]
        ))

        # pick up entrys =============================
        def entryPicker():
            entrysGet = [[]]
            entrys = []
            for widget in self.frameInputsScheduling.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    match widget:
                        case self.valueSchedulingEntry:
                            entrysGet[0].append(self.treating_numbers(widget.get(), 1) if widget.get() != '' else 'R$0,00')
                            entrys.append(widget)
                        case self.timeSchedulingEntry:
                            entrysGet[0].append(self.treating_numbers(widget.get(), 3) if widget.get() != '' else '00:00')
                            entrys.append(widget)
                        case _:
                            entrysGet[0].append(widget.get().upper())
                            entrys.append(widget)
            return [entrysGet, entrys]

        # buttons management ============
        frameBtns = self.tabvieew(self.frameInputsScheduling, 0.675, 0.02, 0.3, 0.9)
        frameBtns.add('Agendamento')
        # add -------------
        addBtn = self.button(frameBtns.tab('Agendamento'), 'Adicionar serviço', 0.225, 0.08, 0.55, 0.2, function=lambda: self.register_scheduling(entryPicker()[0], type_function='add', treeview=self.treeviewScheduling))
        # remove -------------
        removeBtn = self.button(frameBtns.tab('Agendamento'), 'Remover serviço', 0.225, 0.38, 0.55, 0.2, function=lambda: self.register_scheduling(entryPicker()[0], type_function='remove', treeview=self.treeviewScheduling))
        # finish scheduling ---------
        registerBtn = self.button(frameBtns.tab('Agendamento'), 'Finalisar agendamento', 0.225, 0.68, 0.55, 0.2, function=lambda: self.register_scheduling(entryPicker()[0], type_function='finishRegister', treeview=self.treeviewScheduling))

        # events bind for buttons ===========
        self.schedulingFrame.bind_all('<Control-a>', lambda e: self.insert_informations_entrys(entryPicker()[1], insert=False))
        self.schedulingFrame.bind_all('<Control-plus>', lambda e: self.register_scheduling(entryPicker()[0], type_function='add', treeview=self.treeviewScheduling))
        self.schedulingFrame.bind_all('<Control-minus>', lambda e: self.register_scheduling(entryPicker()[0], type_function='remove', treeview=self.treeviewScheduling))
        self.schedulingFrame.bind_all('<Control-f>', lambda e: self.register_scheduling(entryPicker()[0], type_function='finishRegister', treeview=self.treeviewScheduling))

        # frame treeview ==================
        self.frameTreeviewScheduling = self.frame(self.schedulingFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('Cliente', 'Serviço', 'Profissional',  'Valor', 'Método de pagamento', 'Data', 'Horário')
        self.treeviewScheduling = self.treeview(self.frameTreeviewScheduling, informationOfTable)
        self.lineTreeviewColor['scheduling'] = 0'''

    # =================================  informations configuration  ======================================
    def frame_customers(self):
        # frame photo ==========================================
        self.framePhotoClient = self.frame(self.costumersFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelClient = self.labels(self.framePhotoClient, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['costumer'][0], position=CENTER)

        # observation --------------------
        self.observationClientEntry = self.text_box(self.costumersFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsClient = self.frame(self.costumersFrame, 0.14, 0.01, 0.855, 0.43)

        # name -------------
        labelName = self.labels(self.frameInputsClient, 'Nome:', 0.02, 0.08, width=0.08)
        self.nameClientEntry = self.entry(self.frameInputsClient, 0.1, 0.08, 0.2, 0.12, type_entry='entry')

        # birtday -------------
        labelBirtday = self.labels(self.frameInputsClient, 'Nascimento:', 0.02, 0.22, width=0.15)
        self.birtdayClientEntry = self.entry(self.frameInputsClient, 0.14, 0.22, 0.16, 0.12, type_entry='date')

        # cpf -------------
        labelcpf = self.labels(self.frameInputsClient, 'CPF:', 0.02, 0.36, width=0.15)
        self.cpfClientEntry = self.entry(self.frameInputsClient, 0.1, 0.36, 0.20, 0.12, type_entry='entry')

        # children -------------
        labelchildren = self.labels(self.frameInputsClient, 'Filhos:', 0.02, 0.50, width=0.15)
        self.childrenClientBtn = StringVar(value='')
        yes = self.button(
            self.frameInputsClient, 'Sim', 0.11, 0.51, 0.12, 0.1, type_btn='radioButton',
            value='Sim', retur_variable=self.childrenClientBtn
        )
        no = self.button(
            self.frameInputsClient, 'Não', 0.18, 0.51, 0.12, 0.1, type_btn='radioButton',
            value='Não', retur_variable=self.childrenClientBtn
        )

        # phone -------------
        labelPhono = self.labels(self.frameInputsClient, 'Telefone:', 0.02, 0.64, width=0.15)
        self.phoneClientEntry = self.entry(self.frameInputsClient, 0.126, 0.64, 0.173, 0.12, type_entry='entry')

        # firstDate -------------
        labelFirstDate = self.labels(self.frameInputsClient, 'Cliente desde:', 0.02, 0.78, width=0.16)
        self.firstDateClientEntry = self.entry(self.frameInputsClient, 0.159, 0.78, 0.14, 0.12, type_entry='date')

        # adress -----------------
        labelAdress = self.labels(self.frameInputsClient, 'Endereço:', 0.32, 0.08, width=0.16)
        self.adressClientEntry = self.entry(self.frameInputsClient, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # zip code -----------------
        labelZipCode = self.labels(self.frameInputsClient, 'CEP:', 0.32, 0.22, width=0.16)
        self.zipCodeClientEntry = self.entry(self.frameInputsClient, 0.44, 0.22, 0.125, 0.12, type_entry='entry')

        # district -----------------
        labelDistrict = self.labels(self.frameInputsClient, 'Bairro:', 0.32, 0.36, width=0.16)
        self.districtClientEntry = self.entry(self.frameInputsClient, 0.44, 0.36, 0.2, 0.12, type_entry='entry')

        # city -----------------
        labelCity = self.labels(self.frameInputsClient, 'Cidade:', 0.32, 0.50, width=0.16)
        self.cityClientEntry = self.entry(self.frameInputsClient, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # state -----------------
        labelState = self.labels(self.frameInputsClient, 'Estado:', 0.32, 0.64, width=0.16)
        self.stateClientEntry = self.entry(self.frameInputsClient, 0.44, 0.64, 0.2, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsClient, 'Foto:', 0.32, 0.78, width=0.16, color='#803356')
        imageBtn = self.button(
            self.frameInputsClient, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelClient, 'costumer')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsClient, '', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, False, type_insert='advanced', table='Clientes', photo='costumer'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frameInputs =========================
        self.zipCodeClientEntry.bind('<FocusOut>', lambda e: self.request_adrees(entryPicker()[0][7], entryPicker()[1][8:11]))
        self.phoneClientEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.phoneClientEntry, 8))
        self.cpfClientEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.cpfClientEntry, 9))
        # frame treeview ==================
        self.frameTreeviewClient = self.frame(self.costumersFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Nome', 'Nascimento', 'CPF', 'Filhos', 'Telefone', 'Cliente desde', 'Endereço', 'CEP', 'Bairro', 'Cidade', 'Estado')
        self.treeviewClient = self.treeview(self.frameTreeviewClient, informationOfTable)
        self.lineTreeviewColor['client'] = 0
        # event bind treeview ==========================================
        self.treeviewClient.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, type_insert='advanced', table='Clientes', photo='costumer'))

        # save last search schedule ===================================
        self.lastSearch['client'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_client(entryPicker()[0], self.treeviewClient, deleteInformationsInputs),
            'search': lambda: self.search_client(self.treeviewClient, entryPicker()[0]),
            'order': lambda e: self.search_client(self.treeviewClient, entryPicker()[0]),
            'update': lambda: self.update_client(self.treeviewClient, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_client(self.treeviewClient),
            'pdf': lambda: self.create_pdf_client(self.treeviewClient),
            'informations': lambda: self.message_informations_clients(self.treeviewClient)
        }
        self.orderBtnClient = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsClient, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsClient.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # string var informations ======================
            entrysGet.insert(3, self.childrenClientBtn.get())
            entrys.insert(3, self.childrenClientBtn)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['costumer'][1])

            # label photo =================================
            entrys.append(self.labelClient)

            # observations informations ====================
            entrysGet.append(self.observationClientEntry.get("1.0", "end-1c"))
            entrys.append(self.observationClientEntry)

            # order informations and ==========================
            entrysGet.append(self.orderBtnClient.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_client(self.treeviewClient, entryPicker()[0])

    def frame_employers(self):
        # frame photo ==========================================
        self.framePhotoEmployee = self.frame(self.employersFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelProfessional = self.labels(self.framePhotoEmployee, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['employee'][0], position=CENTER)

        # observation --------------------
        self.observationEmployeeEntry = self.text_box(self.employersFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsEmployee = self.frame(self.employersFrame, 0.14, 0.01, 0.855, 0.43)

        # name -------------
        labelName = self.labels(self.frameInputsEmployee, 'Nome:', 0.02, 0.08, width=0.08)
        self.nameEmployeeEntry = self.entry(self.frameInputsEmployee, 0.1, 0.08, 0.2, 0.12, type_entry='entry')

        # cpf -------------
        labelcpf = self.labels(self.frameInputsEmployee, 'CPF:', 0.02, 0.22, width=0.15)
        self.cpfEmployeeEntry = self.entry(self.frameInputsEmployee, 0.1, 0.22, 0.20, 0.12, type_entry='entry')

        # admissom -------------
        labelAdmisson = self.labels(self.frameInputsEmployee, 'Admissão:', 0.02, 0.36, width=0.15)
        self.admissonEmployeeEntry = self.entry(self.frameInputsEmployee, 0.14, 0.36, 0.16, 0.12, type_entry='date')

        # email -------------
        labelEmail = self.labels(self.frameInputsEmployee, 'E-mail:', 0.02, 0.50, width=0.15)
        self.emailEmployeeEntry = self.entry(self.frameInputsEmployee, 0.1, 0.50, 0.2, 0.12, type_entry='entry')

        # phone -------------
        labelPhone = self.labels(self.frameInputsEmployee, 'Telefone:', 0.02, 0.64, width=0.15)
        self.phonoEmployeeEntry = self.entry(self.frameInputsEmployee, 0.126, 0.64, 0.173, 0.12, type_entry='entry')

        # phone emergency -------------
        labelPhoneEmergency = self.labels(self.frameInputsEmployee, 'Emergência:', 0.02, 0.78, width=0.16)
        self.phoneEmergencyEmployeeEntry = self.entry(self.frameInputsEmployee, 0.14, 0.78, 0.159, 0.12, type_entry='entry')

        # adress -----------------
        labelAdress = self.labels(self.frameInputsEmployee, 'Endereço:', 0.32, 0.08, width=0.16)
        self.adressEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # zip code -----------------
        labelZipCode = self.labels(self.frameInputsEmployee, 'CEP:', 0.32, 0.22, width=0.16)
        self.zipCodeEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.22, 0.125, 0.12, type_entry='entry')

        # district -----------------
        labelDistrict = self.labels(self.frameInputsEmployee, 'Bairro:', 0.32, 0.36, width=0.16)
        self.districtEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.36, 0.2, 0.12, type_entry='entry')

        # city -----------------
        labelCity = self.labels(self.frameInputsEmployee, 'Cidade:', 0.32, 0.50, width=0.16)
        self.cityEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # state -----------------
        labelState = self.labels(self.frameInputsEmployee, 'Estado:', 0.32, 0.64, width=0.16)
        self.stateEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.64, 0.2, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsEmployee, 'Foto:', 0.32, 0.78, width=0.16, color='#803356')
        imageBtn = self.button(
            self.frameInputsEmployee, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelProfessional, 'employee')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsEmployee, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, False, type_insert='advanced', table='Profissional', photo='employee'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frameInputs =========================
        self.zipCodeEmployeeEntry.bind('<FocusOut>', lambda e: self.request_adrees(entryPicker()[0][7], entryPicker()[1][8:11]))
        self.phonoEmployeeEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.phonoEmployeeEntry, 8))
        self.phoneEmergencyEmployeeEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.phoneEmergencyEmployeeEntry, 8))
        self.cpfEmployeeEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.cpfEmployeeEntry, 9))

        # frame treeview ==================
        self.frameTreeviewEmployer = self.frame(self.employersFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Nome', 'CPF', 'Admissão', 'E-mail', 'Telefone', 'Emergência', 'Endereço', 'Bairro', 'CEP', 'Cidade', 'Estado')
        self.treeviewEmployer = self.treeview(self.frameTreeviewEmployer, informationOfTable)
        self.lineTreeviewColor['employee'] = 0
        # event bind treeview ==========================================
        self.treeviewEmployer.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewEmployer, type_insert='advanced', table='Profissionais', photo='employee'))

        # save last search schedule ===================================
        self.lastSearch['employee'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_professional(entryPicker()[0], self.treeviewEmployer, deleteInformationsInputs),
            'search': lambda: self.search_professional(self.treeviewEmployer, entryPicker()[0]),
            'order': lambda e: self.search_professional(self.treeviewEmployer, entryPicker()[0]),
            'update': lambda: self.update_professional(self.treeviewEmployer, entryPicker()[0]),
            'delete': lambda: self.delete_professional(self.treeviewEmployer),
            'pdf': lambda: self.create_pdf_professional(self.treeviewEmployer),
            'informations': lambda: self.message_informations_professional(self.treeviewEmployer)
        }
        self.orderBtnEmployer = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsEmployee, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsEmployee.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['employee'][1])

            # label photo =================================
            entrys.append(self.labelProfessional)

            # observations informations ====================
            entrysGet.append(self.observationEmployeeEntry.get("1.0", "end-1c"))
            entrys.append(self.observationEmployeeEntry)

            # order informations and ==========================
            entrysGet.append(self.orderBtnEmployer.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_professional(self.treeviewEmployer, entryPicker()[0])

    def frame_service(self):
        # frame inputs ==========================================
        self.frameInputsService = self.frame(self.servicesFrame, 0.195, 0.01, 0.6, 0.43)

        # name --------------------
        labelService = self.labels(self.frameInputsService, 'Serviço:', 0.07, 0.29, width=0.1)
        self.serviceEntry = self.entry(self.frameInputsService, 0.22, 0.29, 0.2, 0.12, type_entry='entry')

        # price -------------------
        labelPrice = self.labels(self.frameInputsService, 'Valor:', 0.07, 0.49, width=0.1)
        self.priceEntry = self.entry(self.frameInputsService, 0.22, 0.49, 0.2, 0.12, type_entry='entry')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsService, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewService, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewService = self.frame(self.servicesFrame, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Serviço', 'Valor')
        self.treeviewService = self.treeview(self.frameTreeviewService, informationOfTable, max_width=280)
        self.lineTreeviewColor['service'] = 0
        # event bind treeview ==========================================
        self.treeviewService.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewService))

        # save last search schedule ===================================
        self.lastSearch['service'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_service(entryPicker()[0], self.treeviewService, deleteInformationsInputs),
            'search': lambda: self.search_service(self.treeviewService, entryPicker()[0]),
            'order': lambda e: self.search_service(self.treeviewService, entryPicker()[0]),
            'update': lambda: self.update_service(self.treeviewService, entryPicker()[0]),
            'delete': lambda: self.delete_service(self.treeviewService),
            'pdf': lambda: self.create_pdf_service(self.treeviewService),
            'informations': lambda: self.message_informations_service(self.treeviewService)
        }
        self.orderBtnService = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsService, functions, self.photosAndIcons, informationOfTable)

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsService.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            # order =============================================
            entrysGet.append(self.orderBtnService.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_service(self.treeviewService, entryPicker()[0])

    '''def frame_barCode(self):
        # frame photo ==========================================
        self.framePhotoBarCode = self.frame(self.barCodeFrame, 0.02, 0.01, 0.15, 0.3)

        # photo ----------
        self.labelBarCode = self.labels(self.framePhotoBarCode, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['barCode'][0], position=CENTER)

        # observation --------------------
        self.observationBarCodeEntry = self.text_box(self.barCodeFrame, 0.02, 0.32, 0.15, 0.12)

        # frame inputs ==========================================
        self.frameInputsBarCode = self.frame(self.barCodeFrame, 0.175, 0.01, 0.8, 0.43)

        # name --------------------
        labelEmployee = self.labels(self.frameInputsBarCode, 'Profissional:', 0.07, 0.22, width=0.14)
        self.employeeEntry = self.entry(self.frameInputsBarCode, 0.22, 0.22, 0.2, 0.12, type_entry='list')

        # price -------------------
        labelService = self.labels(self.frameInputsBarCode, 'Serviço:', 0.07, 0.42, width=0.1)
        self.serviceEntry = self.entry(self.frameInputsBarCode, 0.22, 0.42, 0.2, 0.12, type_entry='list')

        # barcode -------------------
        labelBarCode = self.labels(self.frameInputsBarCode, 'Código:', 0.07, 0.62, width=0.1)
        self.barCodeEntry = self.entry(self.frameInputsBarCode, 0.22, 0.62, 0.2, 0.12, type_entry='entry')

        # button random -------------
        btnRandom = self.button(
            self.frameInputsBarCode, '', 0.422, 0.607, 0.047, 0.145, photo=self.photosAndIcons['random'][0], type_btn='buttonPhoto', background='white',
            function=lambda: [self.barCodeEntry.delete(0, END), self.barCodeEntry.insert(0, randint(100000000000, 999999999999))]
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsBarCode, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, False, type_insert='advanced', table='Código_de_barras', photo='barCode'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # make collage --------------------
        makeCollage = self.button(
            self.frameInputsBarCode, '', 0.05, 0.87, 0.03, 0.12, function=lambda: self.create_image_colage(),
            photo=self.image('assets/collage.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of inputs ================================
        self.employeeEntry.bind('<KeyPress>', lambda e: self.employeeEntry.configure(
            values=[name[1] for name in self.search_professional(informations=self.searching_list(self.employeeEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))
        self.serviceEntry.bind('<KeyPress>', lambda e: self.serviceEntry.configure(
            values=[name[1] for name in self.search_service(informations=self.searching_list(self.serviceEntry.get(), 1, 'serviço'), save_seacrh=False, insert=False)]
        ))

        # frame treeview ==================
        self.frameTreeviewBarCode = self.frame(self.barCodeFrame, 0.02, 0.45, 0.953, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Profissional', 'Serviço', 'Código')
        self.treeviewBarCode = self.treeview(self.frameTreeviewBarCode, informationOfTable, max_width=350)
        self.lineTreeviewColor['barCode'] = 0
        # event bind treeview ==========================================
        self.treeviewBarCode.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewBarCode, type_insert='advanced', table='Código_de_barras', photo='barCode', size=(250, 200)))

        # save last search schedule ===================================
        self.lastSearch['barCode'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_barCode(entryPicker()[0], self.treeviewBarCode),
            'search': lambda: self.search_barCode(self.treeviewBarCode, entryPicker()[0]),
            'order': lambda e: self.search_barCode(self.treeviewBarCode, entryPicker()[0]),
            'update': lambda: self.update_barCode(self.treeviewBarCode, entryPicker()[0]),
            'delete': lambda: self.delete_barCode(self.treeviewBarCode),
            'pdf': lambda: self.create_pdf_barCode(self.treeviewBarCode),
            'informations': lambda: self.message_informations_barCode(self.treeviewBarCode)
        }
        self.orderBtnBarCode = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsBarCode, functions, self.photosAndIcons, informationOfTable)

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsBarCode.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # label photo =================================
            entrys.append(self.labelBarCode)

            # observations informations ====================
            entrysGet.append(self.observationBarCodeEntry.get("1.0", "end-1c"))
            entrys.append(self.observationBarCodeEntry)

            # order =============================================
            entrysGet.append(self.orderBtnBarCode.get())

            return [entrysGet, entrys]

        # init search =========================
        self.search_barCode(self.treeviewBarCode, entryPicker()[0])'''

    def frame_stock_informations(self):
        # Supplier ========================================
        self.typeStockInformations.add(' Fornecedor ')
        functions = {
            'register': lambda: self.register_InformationsStock(
                ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get(), 'supplier'], self.supplier['treeview'], self.supplier['deleteInputs']
            ),
            'search': lambda: self.search_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor'
            ),
            'update': lambda: self.update_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get()], typeInformations='supplier'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.supplier['treeview'], 'Fornecedores'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.supplier['treeview'], 'Fornecedores'
            )
        }
        self.supplier = self.informations_simple(self.typeStockInformations.tab(' Fornecedor '), 'Fornecedor', ('ID', 'Fornecedor'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['supplier'] = 0
        # event bind treeview ==========================================
        self.supplier['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.supplier['entry']], self.supplier['treeview']))
        # save last search schedule ===================================
        self.lastSearch['supplier'] = ''

        # Brand ========================================
        self.typeStockInformations.add(' Marca ')
        functions = {
            'register': lambda: self.register_InformationsStock(
                ['Marca', self.brand['entry'].get(), self.brand['order'].get(), 'brand'], self.brand['treeview'], self.brand['deleteInputs']
            ),
            'search': lambda: self.search_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca'
            ),
            'update': lambda: self.update_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get()], typeInformations='brand'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.brand['treeview'], 'Marcas'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.brand['treeview'], 'Marcas'
            )
        }
        self.brand = self.informations_simple(self.typeStockInformations.tab(' Marca '), 'Marca', ('ID', 'Marca'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['brand'] = 0
        # event bind treeview ==========================================
        self.brand['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.brand['entry']], self.brand['treeview']))
        # save last search schedule ===================================
        self.lastSearch['brand'] = ''

        # Typr ========================================
        self.typeStockInformations.add(' Produto ')
        functions = {
            'register': lambda: self.register_InformationsStock(['Tipo', self.type['entry'].get(), self.type['order'].get(), 'supplier'], self.type['treeview'], self.type['deleteInputs']),
            'search': lambda: self.search_InformationsStock(
                self.type['treeview'], ['Tipo', self.type['entry'].get(), self.type['order'].get()], typeInformations='type', table='Tipo'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.type['treeview'], ['Tipo', self.type['entry'].get(), self.type['order'].get()], typeInformations='type', table='Tipo'
            ),
            'update': lambda: self.update_InformationsStock(
                self.type['treeview'], ['Tipo', self.type['entry'].get()], typeInformations='type'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.type['treeview'], ['Tipo', self.type['entry'].get(), self.type['order'].get()], typeInformations='type', table='Tipo'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.type['treeview'], 'Tipos'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.supplier['treeview'], 'Tipos'
            )
        }
        self.type = self.informations_simple(self.typeStockInformations.tab(' Produto '), 'Produto', ('ID', 'Produto'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['type'] = 0
        # event bind treeview ==========================================
        self.type['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.type['entry']], self.type['treeview']))
        # save last search schedule ===================================
        self.lastSearch['type'] = ''

        # measure ========================================
        self.typeStockInformations.add(' Medida ')
        functions = {
            'register': lambda: self.register_InformationsStock(
                ['Medida', self.measure['entry'].get(), self.measure['order'].get(), 'measure'], self.measure['treeview'], self.measure['deleteInputs']
            ),
            'search': lambda: self.search_InformationsStock(
                self.measure['treeview'], ['Medida', self.measure['entry'].get(), self.measure['order'].get()], typeInformations='measure', table='Medida'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.measure['treeview'], ['Medida', self.measure['entry'].get(), self.measure['order'].get()], typeInformations='measure', table='Medida'
            ),
            'update': lambda: self.update_InformationsStock(
                self.measure['treeview'], ['Medida', self.measure['entry'].get()], typeInformations='measure'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.measure['treeview'], ['Medida', self.measure['entry'].get(), self.measure['order'].get()], typeInformations='measure', table='Medida'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.measure['treeview'], 'Medidas'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.measure['treeview'], 'Medidas'
            )
        }
        self.measure = self.informations_simple(self.typeStockInformations.tab(' Medida '), 'Medida', ('ID', 'Medida'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['measure'] = 0
        # event bind treeview ==========================================
        self.measure['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.measure['entry']], self.measure['treeview']))

        # save last search schedule ===================================
        self.lastSearch['measure'] = ''

        # init search for day ===============================================
        self.search_init()

    def frame_users(self):
        # frame inputs =========================================
        self.frameInputsUsers = self.frame(self.userFrame, 0.195, 0.01, 0.6, 0.43)

        # user --------------------
        labelUser = self.labels(self.frameInputsUsers, 'Usuário:', 0.07, 0.25, width=0.1)
        self.userEntry = self.entry(self.frameInputsUsers, 0.20, 0.25, 0.23, 0.12, type_entry='entry')

        # password -------------------
        labelPassword = self.labels(self.frameInputsUsers, 'Senha:', 0.07, 0.45, width=0.1)
        self.passwordEntry = self.entry(self.frameInputsUsers, 0.20, 0.45, 0.23, 0.12, type_entry='entry')

        # level -------------------
        labelLevel = self.labels(self.frameInputsUsers, 'Nivel:', 0.07, 0.65, width=0.1)
        self.levelEntry = self.entry(
            self.frameInputsUsers, 0.20, 0.65, 0.23, 0.12, type_entry='list',
            value=['ADMINISTRADOR', 'USUÀRIO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsUsers, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewService, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewUsers = self.frame(self.userFrame, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Usuário', 'Senha', 'Nivel')
        self.treeviewUsers = self.treeview(self.frameTreeviewUsers, informationOfTable, max_width=280)
        self.lineTreeviewColor['users'] = 0
        # event bind treeview ==========================================
        self.treeviewUsers.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers))

        # save last search schedule ===================================
        self.lastSearch['users'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(self.register_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'search': lambda: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'order': lambda e: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'update': lambda: self.password_window(self.update_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_users, {'treeview': self.treeviewUsers}),
            'pdf': lambda: self.create_pdf_service(self.treeviewUsers),
            'informations': lambda: self.message_informations_service(self.treeviewUsers)
        }
        self.buttons = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsUsers, functions, self.photosAndIcons, informationOfTable, treeview='no')

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsUsers.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            return [entrysGet, entrys]

        # init search for day ===============================================
        # self.search_service(self.treeviewService, entryPicker()[0])

    # =================================  stock configuration  ======================================
    def frame_use_inventory_control(self):
        # frame photo ==========================================
        self.framePhotoUseInventoryControl = self.frame(self.typeStockmanagement.tab(' Estoque de uso '), 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelUseProduct = self.labels(self.framePhotoUseInventoryControl, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['productUse'][0], position=CENTER)

        # observation --------------------
        self.observationUseinventoryControlEntry = self.text_box(self.typeStockmanagement.tab(' Estoque de uso '), 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsUseInventoryControl = self.frame(self.typeStockmanagement.tab(' Estoque de uso '), 0.14, 0.01, 0.855, 0.43)

        # supplier -------------
        labelSupplier = self.labels(self.frameInputsUseInventoryControl, 'Fornecedor:', 0.02, 0.08, width=0.12)
        self.supplierUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.14, 0.08, 0.18, 0.12, type_entry='list')

        # brand -------------
        labelbrand = self.labels(self.frameInputsUseInventoryControl, 'Marca:', 0.02, 0.22, width=0.15)
        self.brandUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.14, 0.22, 0.18, 0.12, type_entry='list')

        # type -------------
        labelType = self.labels(self.frameInputsUseInventoryControl, 'Produto:', 0.02, 0.36, width=0.15)
        self.typeUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.14, 0.36, 0.18, 0.12, type_entry='list')

        # amount -------------
        labelAmount = self.labels(self.frameInputsUseInventoryControl, 'Quantidade:', 0.02, 0.50, width=0.15)
        self.amountnUseIventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.14, 0.50, 0.16, 0.12, type_entry='entry')

        # measure -------------
        labelmeasure = self.labels(self.frameInputsUseInventoryControl, 'Medida:', 0.02, 0.64, width=0.15)
        self.measureUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.14, 0.64, 0.18, 0.12, type_entry='list')

        # value -------------
        labelValue = self.labels(self.frameInputsUseInventoryControl, 'Valor:', 0.02, 0.78, width=0.16)
        self.valueInputsUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.14, 0.78, 0.159, 0.12, type_entry='entry')

        # validity -----------------
        labelValidity = self.labels(self.frameInputsUseInventoryControl, 'Validade:', 0.34, 0.08, width=0.16)
        self.validitytUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.45, 0.08, 0.14, 0.12, type_entry='date', validity='yes')

        # exit -----------------
        labelexit = self.labels(self.frameInputsUseInventoryControl, 'Saída:', 0.34, 0.22, width=0.16, color='#803356')
        self.exitInputsUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.45, 0.22, 0.189, 0.12, type_entry='entry')

        # remainingAmount -----------------
        labelRemainingAmount = self.labels(self.frameInputsUseInventoryControl, 'Q/Restante:', 0.34, 0.36, width=0.16, color='#803356')
        self.remainingAmountUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.45, 0.36, 0.189, 0.12, type_entry='entry')

        # entry -----------------
        labelEntry = self.labels(self.frameInputsUseInventoryControl, 'Entrada:', 0.34, 0.50, width=0.16, color='#803356')
        self.entryUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # modify -----------------
        labelModify = self.labels(self.frameInputsUseInventoryControl, 'Modificação:', 0.34, 0.64, width=0.16, color='#803356')
        self.modifyUseInventoryControlEntry = self.entry(self.frameInputsUseInventoryControl, 0.46, 0.64, 0.1794, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsUseInventoryControl, 'Foto:', 0.34, 0.78, width=0.16, color='#803356')
        imageBtn = self.button(
            self.frameInputsUseInventoryControl, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelUseProduct, 'productUse')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsUseInventoryControl, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUseInventoryControl, False, type_insert='advanced', table='Estoque_de_uso', photo='productUse', data_base='stock'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewUseInventoryControl = self.frame(self.typeStockmanagement.tab(' Estoque de uso '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Fornecedor', 'Marca',  'Produto', 'Quantidade', 'Medida', 'Valor', 'Validade', 'Saída', 'Q/Restante', 'Entrada', 'Modificação')
        self.treeviewUseInventoryControl = self.treeview(self.frameTreeviewUseInventoryControl, informationOfTable)
        self.lineTreeviewColor['productUse'] = 0
        # event bind treeview ==========================================
        self.treeviewUseInventoryControl.bind(
            "<Double-Button-1>", lambda e: [
                self.insert_informations_entrys(entryPicker()[1], self.treeviewUseInventoryControl, type_insert='advanced', table='Estoque_de_uso', photo='productUse', data_base='stock'),
                self.exitInputsUseInventoryControlEntry.delete(0, END),
                self.exitInputsUseInventoryControlEntry.insert(0, "0")
            ]
        )
        self.treeviewUseInventoryControl.bind(
            "<Control-s>", lambda e: self.select_finished_and_defeated(self.treeviewUseInventoryControl, 'usageStock')
        )

        # save last search schedule ===================================
        self.lastSearch['productUse'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_stock(entryPicker()[0], self.treeviewUseInventoryControl, sqlRegister=registerUsageStock, table='Estoque_de_uso', typeStock='productUse', button=deleteInformationsInputs),
            'search': lambda: self.search_stock(self.treeviewUseInventoryControl, entryPicker()[0], typeStock='productUse', sqlSearch=searchUsageStock),
            'order': lambda e: self.search_stock(self.treeviewUseInventoryControl, entryPicker()[0], typeStock='productUse', sqlSearch=searchUsageStock),
            'update': lambda: self.password_window(
                self.update_stock, {
                    'treeview': self.treeviewUseInventoryControl,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateUsageStock,
                        'typeStock': "productUse",
                        'table': 'Estoque_de_uso'
                    }
                }
            ),
            'delete': lambda: self.password_window(self.delete_stock, parameter={
                'treeview': self.treeviewUseInventoryControl,
                'register_in_unusable': True,
                'treeview2': self.treeviewUseInventoryControlUnusable,
                'parameters': {
                    'table': 'Estoque_de_uso',
                    'typeStock': 'productUse',

                }
            }),
            'pdf': lambda: self.create_pdf_stock(
                self.treeviewUseInventoryControl, tablePart1=tableWithInformationsUsageStockTreeview1, tablePart2=tableWithInformationsUsageStockTreeview2,
                supplementaryTable=tableWithInformationsComplementaryUsageStock, typeStock='usageStock'
            ),
            'informations': lambda: self.message_informations_stock(self.treeviewUseInventoryControl, typeMessage=messageUseStock, typeStock='usageStock')
        }
        self.orderBtnUseIventoryControl = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsUseInventoryControl, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsUseInventoryControl.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['productUse'][1])

            # label photo =================================
            entrys.append(self.labelUseProduct)

            # observations informations ====================
            entrysGet.append(self.observationUseinventoryControlEntry.get("1.0", "end-1c"))
            entrys.append(self.observationUseinventoryControlEntry)

            # order =============================================
            entrysGet.append(self.orderBtnUseIventoryControl.get())
            return [entrysGet, entrys]

        # init search =================================
        self.search_stock(self.treeviewUseInventoryControl, entryPicker()[0], typeStock='productUse', sqlSearch=searchUsageStock)

    def frame_sale_inventory_control(self):
        # frame photo ==========================================
        self.framePhotoSaleInventoryControl = self.frame(self.typeStockmanagement.tab(' Estoque de venda '), 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelSaleProduct = self.labels(self.framePhotoSaleInventoryControl, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['productSale'][0], position=CENTER)

        # observation --------------------
        self.observationSaleinventoryControlEntry = self.text_box(self.typeStockmanagement.tab(' Estoque de venda '), 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsSaleInventoryControl = self.frame(self.typeStockmanagement.tab(' Estoque de venda '), 0.14, 0.01, 0.855, 0.43)

        # supplier -------------
        labelSupplier = self.labels(self.frameInputsSaleInventoryControl, 'Fornecedor:', 0.02, 0.08, width=0.12)
        self.supplierSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.08, 0.18, 0.12, type_entry='list')

        # brand -------------
        labelBrand = self.labels(self.frameInputsSaleInventoryControl, 'Marca:', 0.02, 0.22, width=0.15)
        self.brandSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.22, 0.18, 0.12, type_entry='list')

        # type -------------
        labelType = self.labels(self.frameInputsSaleInventoryControl, 'Produto:', 0.02, 0.36, width=0.15)
        self.typeSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.36, 0.18, 0.12, type_entry='list')

        # amount -------------
        labelamount = self.labels(self.frameInputsSaleInventoryControl, 'Quantidade:', 0.02, 0.50, width=0.15)
        self.amounrSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.50, 0.16, 0.12, type_entry='entry')

        # measure -------------
        labelMeasure = self.labels(self.frameInputsSaleInventoryControl, 'Medida:', 0.02, 0.64, width=0.16)
        self.measureSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.64, 0.18, 0.12, type_entry='list')

        # buy -----------------
        labelBuy = self.labels(self.frameInputsSaleInventoryControl, 'V/compra:', 0.02, 0.78, width=0.16)
        self.buySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.78, 0.16, 0.12, type_entry='entry')

        # sale -----------------
        labelsale = self.labels(self.frameInputsSaleInventoryControl, 'V/venda:', 0.34, 0.08, width=0.16)
        self.saleInputsSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # validity -----------------
        labelValidity = self.labels(self.frameInputsSaleInventoryControl, 'Validade:', 0.34, 0.22, width=0.16)
        self.validitySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.44, 0.22, 0.14, 0.12, type_entry='date', validity='yes')

        # custom -------------
        labelCustom = self.labels(self.frameInputsSaleInventoryControl, 'Cliente:', 0.34, 0.36, width=0.15, color='#803356')
        self.customSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.44, 0.36, 0.2, 0.12, type_entry='list')

        # method pay -----------------
        labelMethodPay = self.labels(self.frameInputsSaleInventoryControl, 'M/Pagamento:', 0.34, 0.50, width=0.16, color='#803356')
        self.methodPaySaleInventoryControlEntry = self.entry(
            self.frameInputsSaleInventoryControl, 0.47, 0.50, 0.17, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # entry -----------------
        labelEntry = self.labels(self.frameInputsSaleInventoryControl, 'Entrada:', 0.34, 0.64, width=0.16, color='#803356')
        self.entrySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.64, 0.1794, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsSaleInventoryControl, 'Foto:', 0.34, 0.78, width=0.16, color='#803356')
        imageBtn = self.button(
            self.frameInputsSaleInventoryControl, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelSaleProduct, 'productSale')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSaleInventoryControl, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUseInventoryControl, False, type_insert='advanced', table='Estoque_de_venda', photo='productSale', data_base='stock'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of inputs ====================
        self.customSaleInventoryControlEntry.bind('<KeyPress>', lambda e: self.customSaleInventoryControlEntry.configure(
            values=[name[1] for name in self.search_client(informations=self.searching_list(self.customSaleInventoryControlEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))

        # frame treeview ==================
        self.frameTreeviewSaleInventoryControl = self.frame(self.typeStockmanagement.tab(' Estoque de venda '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Fornecedor', 'Marca', 'Produto', 'Quantidade', 'Medida', 'V/compra', 'V/venda', 'Validade', 'Cliente', 'Método de Pagamento', 'Entrada', 'Modificação')
        self.treeviewSaleInventoryControl = self.treeview(self.frameTreeviewSaleInventoryControl, informationOfTable)
        self.lineTreeviewColor['productSale'] = 0
        # event bind treeview ==========================================
        self.treeviewSaleInventoryControl.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewSaleInventoryControl, type_insert='advanced', table='Estoque_de_venda', photo='productSale', data_base='stock')
        )
        self.treeviewSaleInventoryControl.bind(
            "<Control-s>", lambda e: self.select_finished_and_defeated(self.treeviewSaleInventoryControl, 'usageStock')
        )

        # save last search schedule ===================================
        self.lastSearch['productSale'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_stock(entryPicker()[0], self.treeviewSaleInventoryControl, sqlRegister=registerSaleStock, table='Estoque_de_venda', typeStock='productSale', column='entrada', button=deleteInformationsInputs),
            'search': lambda: self.search_stock(self.treeviewSaleInventoryControl, entryPicker()[0], typeStock='productSale', sqlSearch=searchSaleStock),
            'order': lambda e: self.search_stock(self.treeviewSaleInventoryControl, entryPicker()[0], typeStock='productSale', sqlSearch=searchSaleStock),
            'update': lambda: self.password_window(
                self.update_stock, {
                    'treeview': self.treeviewSaleInventoryControl,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateSaleStock,
                        'typeStock': "productSale",
                    }
                }
            ),
            'sale': lambda: [
                self.entrySaleInventoryControlEntry.delete(0, END),
                self.register_stock(entryPicker()[0], self.treeviewSaleInventoryControlUnusable, sqlRegister=registerSaleStockUnusable, table='Estoque_de_vendidos', typeStock='productSaleSold', delete=True, column='venda'),
            ],
            'delete': lambda: self.password_window(self.delete_stock, parameter={
                'treeview': self.treeviewSaleInventoryControl,
                'register_in_unusable': False,
                'treeview2': None,
                'parameters': {
                    'table': 'Estoque_de_venda',
                    'typeStock': 'productSale',
                    'column': 'ID'
                }
            }),
            'pdf': lambda: self.create_pdf_stock(
                self.treeviewSaleInventoryControl, tablePart1=tableWithInformationsSaleStockTreeview1, tablePart2=tableWithInformationsSaleStockTreeview2,
                supplementaryTable=tableWithInformationsComplementarySaleStock, typeStock='saleStock'
            ),
            'informations': lambda: self.message_informations_stock(self.treeviewSaleInventoryControl, typeMessage=messageSaleStock, typeStock='saleStock')
        }
        self.orderBtnSaleIventoryControl = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSaleInventoryControl, functions, self.photosAndIcons, informationOfTable, type_btns='sale')

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsSaleInventoryControl.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['productSale'][1])

            # label photo =================================
            entrys.append(self.labelSaleProduct)

            # observations informations ====================
            entrysGet.append(self.observationSaleinventoryControlEntry.get("1.0", "end-1c"))
            entrys.append(self.observationSaleinventoryControlEntry)

            # order =============================================
            entrysGet.append(self.orderBtnSaleIventoryControl.get())
            return [entrysGet, entrys]

        # init search =================================
        self.search_stock(self.treeviewSaleInventoryControl, entryPicker()[0], typeStock='productSale', sqlSearch=searchSaleStock)

    # ================================== stock unusable configuration ==============================

    def frame_use_inventory_control_unusable(self):
        # frame photo ==========================================
        self.framePhotoUseInventoryControlUnusable = self.frame(self.typeStockUnusableManagement.tab(' Estoque de usados '), 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelUseProductUnusable = self.labels(self.framePhotoUseInventoryControlUnusable, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['productUseUnusable'][0], position=CENTER)

        # observation --------------------
        self.observationUseinventoryControlUnusableEntry = self.text_box(self.typeStockUnusableManagement.tab(' Estoque de usados '), 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsUseInventoryControlUnusable = self.frame(self.typeStockUnusableManagement.tab(' Estoque de usados '), 0.14, 0.01, 0.855, 0.43)

        # supplier -------------
        labelSupplier = self.labels(self.frameInputsUseInventoryControlUnusable, 'Fornecedor:', 0.02, 0.08, width=0.12)
        self.supplierUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.14, 0.08, 0.18, 0.12, type_entry='list')

        # brand -------------
        labelbrand = self.labels(self.frameInputsUseInventoryControlUnusable, 'Marca:', 0.02, 0.22, width=0.15)
        self.brandUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.14, 0.22, 0.18, 0.12, type_entry='list')

        # type -------------
        labelType = self.labels(self.frameInputsUseInventoryControlUnusable, 'Produto:', 0.02, 0.36, width=0.15)
        self.typeUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.14, 0.36, 0.18, 0.12, type_entry='list')

        # amount -------------
        labelAmount = self.labels(self.frameInputsUseInventoryControlUnusable, 'Quantidade:', 0.02, 0.50, width=0.15)
        self.amountnUseIventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.14, 0.50, 0.16, 0.12, type_entry='entry')

        # measure -------------
        labelmeasure = self.labels(self.frameInputsUseInventoryControlUnusable, 'Medida:', 0.02, 0.64, width=0.15)
        self.measureUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.14, 0.64, 0.18, 0.12, type_entry='list')

        # value -------------
        labelValue = self.labels(self.frameInputsUseInventoryControlUnusable, 'Valor:', 0.02, 0.78, width=0.16)
        self.valueInputsUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.14, 0.78, 0.159, 0.12, type_entry='entry')

        # validity -----------------
        labelValidity = self.labels(self.frameInputsUseInventoryControlUnusable, 'Validade:', 0.34, 0.08, width=0.16)
        self.validitytUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.45, 0.08, 0.14, 0.12, type_entry='date', validity='yes')

        # exit -----------------
        labelExit = self.labels(self.frameInputsUseInventoryControlUnusable, 'Saída:', 0.34, 0.22, width=0.16, color='#803356')
        self.exitInputsUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.45, 0.22, 0.189, 0.12, type_entry='entry')

        # remainingAmount -----------------
        labelRemainingAmount = self.labels(self.frameInputsUseInventoryControlUnusable, 'Q/Restante:', 0.34, 0.36, width=0.16, color='#803356')
        self.remainingAmountUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.45, 0.36, 0.189, 0.12, type_entry='entry')

        # date exit -----------------
        labelDateExit = self.labels(self.frameInputsUseInventoryControlUnusable, 'D/Saída:', 0.34, 0.50, width=0.16, color='#803356')
        self.dateExitUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # modify -----------------
        labelModify = self.labels(self.frameInputsUseInventoryControlUnusable, 'Modificação:', 0.34, 0.64, width=0.16, color='#803356')
        self.modifyUseInventoryControlUnusableEntry = self.entry(self.frameInputsUseInventoryControlUnusable, 0.46, 0.64, 0.1794, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsUseInventoryControlUnusable, 'Foto:', 0.34, 0.78, width=0.16, color='#803356')
        imageBtn = self.button(
            self.frameInputsUseInventoryControlUnusable, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelUseProductUnusable, 'productUseUnusable')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsUseInventoryControlUnusable, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUseInventoryControlUnusable, False, type_insert='advanced', table='Estoque_de_inutilizáveis', photo='productUseUnusable', data_base='stock'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewUseInventoryControlUnusable = self.frame(self.typeStockUnusableManagement.tab(' Estoque de usados '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Fornecedor', 'Marca', 'Produto', 'Quantidade', 'Medida', 'Valor', 'Validade', 'Saída', 'Q/Restante', 'D/Saída', 'Modificação')
        self.treeviewUseInventoryControlUnusable = self.treeview(self.frameTreeviewUseInventoryControlUnusable, informationOfTable)
        self.lineTreeviewColor['productUseUnusable'] = 0
        # event bind treeview ==========================================
        self.treeviewUseInventoryControlUnusable.bind(
            "<Double-Button-1>", lambda e: [
                self.insert_informations_entrys(entryPicker()[1], self.treeviewUseInventoryControlUnusable, type_insert='advanced', table='Estoque_de_inutilizáveis', photo='productUseUnusable', data_base='stock'),
                self.exitInputsUseInventoryControlUnusableEntry.delete(0, END),
                self.exitInputsUseInventoryControlUnusableEntry.insert(0, "0")
            ]
        )

        # save last search schedule ===================================
        self.lastSearch['productUseUnusable'] = ''

        # buttons management ============
        functions = {
            'search': lambda: self.search_stock(self.treeviewUseInventoryControlUnusable, entryPicker()[0], typeStock='productUseUnusable', sqlSearch=searchUsageStockUnusable, button=deleteInformationsInputs),
            'order': lambda e: self.search_stock(self.treeviewUseInventoryControlUnusable, entryPicker()[0], typeStock='productUseUnusable', sqlSearch=searchUsageStockUnusable),
            'update': lambda: self.password_window(
                self.update_stock, {
                    'treeview': self.treeviewUseInventoryControlUnusable,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateUsageStockUnusable,
                        'typeStock': "productUseUnusable",
                        'table': 'Estoque_de_inutilizáveis'
                    }
                }
            ),
            'delete': lambda: self.password_window(self.delete_stock, parameter={
                'treeview': self.treeviewUseInventoryControlUnusable,
                'register_in_unusable': False,
                'treeview2': None,
                'parameters': {
                    'table': 'Estoque_de_inutilizáveis',
                    'typeStock': 'productUseUnusable',
                }
            }),
            'pdf': lambda: self.create_pdf_stock(
                self.treeviewUseInventoryControlUnusable, tablePart1=tableWithInformationsUsageStockUnusableTreeview1, tablePart2=tableWithInformationsUsageStockUnusableTreeview2,
                supplementaryTable=tableWithInformationsComplementaryUsageStockUnusable, typeStock='usageStock'
            ),
            'informations': lambda: self.message_informations_stock(self.treeviewUseInventoryControlUnusable, typeMessage=messageUseStock, typeStock='usageStock')
        }
        self.orderBtnUseIventoryControlUnusable = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsUseInventoryControlUnusable, functions, self.photosAndIcons, informationOfTable, type_btns='management')

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsUseInventoryControlUnusable.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['productUseUnusable'][1])

            # label photo =================================
            entrys.append(self.labelUseProductUnusable)

            # observations informations ====================
            entrysGet.append(self.observationUseinventoryControlUnusableEntry.get("1.0", "end-1c"))
            entrys.append(self.observationUseinventoryControlUnusableEntry)

            # order =============================================
            entrysGet.append(self.orderBtnUseIventoryControlUnusable.get())
            return [entrysGet, entrys]

        # init search =================================
        self.search_stock(self.treeviewUseInventoryControlUnusable, entryPicker()[0], typeStock='productUseUnusable', sqlSearch=searchUsageStockUnusable)

    def frame_sale_inventory_control_unusable(self):
        # frame photo ==========================================
        self.framePhotoSaleInventoryControlUnusable = self.frame(self.typeStockUnusableManagement.tab(' Estoque de vendidos '), 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelSaleProductUnusable = self.labels(self.framePhotoSaleInventoryControlUnusable, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['productSaleSold'][0], position=CENTER)

        # observation --------------------
        self.observationSaleinventoryControlUnusableEntry = self.text_box(self.typeStockUnusableManagement.tab(' Estoque de vendidos '), 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsSaleInventoryControlUnusable = self.frame(self.typeStockUnusableManagement.tab(' Estoque de vendidos '), 0.14, 0.01, 0.855, 0.43)

        # supplier -------------
        labelSupplier = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Fornecedor:', 0.02, 0.08, width=0.12)
        self.supplierSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.14, 0.08, 0.18, 0.12, type_entry='list')

        # brand -------------
        labelBrand = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Marca:', 0.02, 0.22, width=0.15)
        self.brandSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.14, 0.22, 0.18, 0.12, type_entry='list')

        # type -------------
        labelType = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Produto:', 0.02, 0.36, width=0.15)
        self.typeSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.14, 0.36, 0.18, 0.12, type_entry='list')

        # amount -------------
        labelamount = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Quantidade:', 0.02, 0.50, width=0.15)
        self.amounrSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.14, 0.50, 0.16, 0.12, type_entry='entry')

        # measure -------------
        labelMeasure = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Medida:', 0.02, 0.64, width=0.16)
        self.measureSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.14, 0.64, 0.18, 0.12, type_entry='list')

        # buy -----------------
        labelBuy = self.labels(self.frameInputsSaleInventoryControlUnusable, 'V/compra:', 0.02, 0.78, width=0.16)
        self.buySaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.14, 0.78, 0.16, 0.12, type_entry='entry')

        # sale -----------------
        labelsale = self.labels(self.frameInputsSaleInventoryControlUnusable, 'V/venda:', 0.34, 0.08, width=0.16)
        self.saleInputsSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # validity -----------------
        labelValidity = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Validade:', 0.34, 0.22, width=0.16)
        self.validitySaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.44, 0.22, 0.14, 0.12, type_entry='date', validity='yes')

        # custom -------------
        labelCustom = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Cliente:', 0.34, 0.36, width=0.15, color='#803356')
        self.customSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.44, 0.36, 0.2, 0.12, type_entry='list')

        # sold -----------------
        labelMethodPay = self.labels(self.frameInputsSaleInventoryControlUnusable, 'M/Pagamento:', 0.34, 0.50, width=0.16, color='#803356')
        self.MethodPaySaleInventoryControlUnusableEntry = self.entry(
            self.frameInputsSaleInventoryControlUnusable, 0.47, 0.50, 0.17, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # modify -----------------
        labelold = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Venda:', 0.34, 0.64, width=0.16, color='#803356')
        self.soldSaleInventoryControlUnusableEntry = self.entry(self.frameInputsSaleInventoryControlUnusable, 0.46, 0.64, 0.1794, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsSaleInventoryControlUnusable, 'Foto:', 0.34, 0.78, width=0.16, color='#803356')
        imageBtn = self.button(
            self.frameInputsSaleInventoryControlUnusable, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelSaleProductUnusable, 'productSaleSold')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSaleInventoryControlUnusable, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUseInventoryControlUnusable, False, type_insert='advanced', table='Estoque_de_vendidos', photo='productSaleSold', data_base='stock'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of inputs ====================
        self.customSaleInventoryControlUnusableEntry.bind('<KeyPress>', lambda e: self.customSaleInventoryControlUnusableEntry.configure(
            values=[name[1] for name in self.search_client(informations=self.searching_list(self.customSaleInventoryControlUnusableEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))

        # frame treeview ==================
        self.frameTreeviewSaleInventoryControlUnusable = self.frame(self.typeStockUnusableManagement.tab(' Estoque de vendidos '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Fornecedor', 'Marca', 'Produto', 'Quantidade', 'Medida', 'V/compra', 'V/venda', 'Validade', 'Cliente', 'Método de Pagamento', 'Venda', 'Modificação')
        self.treeviewSaleInventoryControlUnusable = self.treeview(self.frameTreeviewSaleInventoryControlUnusable, informationOfTable)
        self.lineTreeviewColor['productSaleSold'] = 0
        # event bind treeview ==========================================
        self.treeviewSaleInventoryControlUnusable.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewSaleInventoryControlUnusable, type_insert='advanced', table='Estoque_de_vendidos', photo='productSaleSold', data_base='stock')
        )

        # save last search schedule ===================================
        self.lastSearch['productSaleSold'] = ''

        # buttons management ============
        functions = {
            'search': lambda: self.search_stock(self.treeviewSaleInventoryControlUnusable, entryPicker()[0], typeStock='productSaleSold', sqlSearch=searchSaleStockUnusable, button=deleteInformationsInputs),
            'order': lambda e: self.search_stock(self.treeviewSaleInventoryControlUnusable, entryPicker()[0], typeStock='productSaleSold', sqlSearch=searchSaleStockUnusable),
            'update': lambda: self.password_window(
                self.update_stock, {
                    'treeview': self.treeviewSaleInventoryControlUnusable,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateSaleStockUnusable,
                        'typeStock': "productSaleSold",
                    }
                }
            ),
            'delete': lambda: self.password_window(self.delete_stock, parameter={
                'treeview': self.treeviewSaleInventoryControlUnusable,
                'register_in_unusable': False,
                'treeview2': None,
                'parameters': {
                    'table': 'Estoque_de_vendidos',
                    'typeStock': 'productSaleSold',
                    'column': 'venda'
                }
            }),
            'pdf': lambda: self.create_pdf_stock(
                self.treeviewSaleInventoryControlUnusable, tablePart1=tableWithInformationsSaleStockUnusableTreeview1, tablePart2=tableWithInformationsSaleStockUnusableTreeview2,
                supplementaryTable=tableWithInformationsComplementarySaleStockUnusable, typeStock='saleStock'
            ),
            'informations': lambda: self.message_informations_stock(self.treeviewSaleInventoryControlUnusable, typeMessage=messageSaleStock, typeStock='saleStock')
        }
        self.orderBtnSaleIventoryControlUnusable = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSaleInventoryControlUnusable, functions, self.photosAndIcons, informationOfTable, type_btns='management')

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsSaleInventoryControlUnusable.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['productSaleSold'][1])

            # label photo =================================
            entrys.append(self.labelSaleProductUnusable)

            # observations informations ====================
            entrysGet.append(self.observationSaleinventoryControlUnusableEntry.get("1.0", "end-1c"))
            entrys.append(self.observationSaleinventoryControlUnusableEntry)

            # order =============================================
            entrysGet.append(self.orderBtnSaleIventoryControlUnusable.get())
            return [entrysGet, entrys]

        # init search =================================
        self.search_stock(self.treeviewSaleInventoryControlUnusable, entryPicker()[0], typeStock='productSaleSold', sqlSearch=searchSaleStockUnusable)

    # ================================== cash register configuration ===============================

    def frame_cash_register_management_day(self):

        # frame inputs ==========================================
        self.frameInputsCashDay = self.frame(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.30, 0.01, 0.70, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashDay, 'T/Cliente:', 0.02, 0.08, width=0.12)
        self.customDayEntry = self.entry(self.frameInputsCashDay, 0.16, 0.08, 0.18, 0.12, type_entry='entry')

        # produty -------------
        labelProduty = self.labels(self.frameInputsCashDay, 'T/Produto:', 0.02, 0.22, width=0.15)
        self.productDayEntry = self.entry(self.frameInputsCashDay, 0.16, 0.22, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashDay, 'T/Cartão:', 0.02, 0.36, width=0.15)
        self.cardDayEntry = self.entry(self.frameInputsCashDay, 0.16, 0.36, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashDay, 'T/Dinheiro:', 0.02, 0.50, width=0.15)
        self.moneyDayEntry = self.entry(self.frameInputsCashDay, 0.16, 0.50, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashDay, 'T/Transferência:', 0.02, 0.64, width=0.18)
        self.transferDayEntry = self.entry(self.frameInputsCashDay, 0.21, 0.64, 0.13, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashDay, 'T/Nota:', 0.02, 0.78, width=0.16)
        self.noteDayEntry = self.entry(self.frameInputsCashDay, 0.16, 0.78, 0.18, 0.12, type_entry='entry')

        # Permute -------------
        labelPermute = self.labels(self.frameInputsCashDay, 'T/Permuta:', 0.36, 0.08, width=0.16)
        self.permuteDayEntry = self.entry(self.frameInputsCashDay, 0.485, 0.08, 0.175, 0.12, type_entry='entry')

        # to receive -----------------
        labelCash = self.labels(self.frameInputsCashDay, 'F/Caixa:', 0.36, 0.22, width=0.16)
        self.CashDayEntry = self.entry(self.frameInputsCashDay, 0.47, 0.22, 0.19, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashDay, 'T/Recebido:', 0.36, 0.36, width=0.16)
        self.receivedDayEntry = self.entry(self.frameInputsCashDay, 0.495, 0.36, 0.165, 0.12, type_entry='entry')

        # date -----------------
        labelDate = self.labels(self.frameInputsCashDay, 'Data:', 0.36, 0.50, width=0.16)
        self.dateDayEntry = self.entry(self.frameInputsCashDay, 0.47, 0.50, 0.14, 0.12, type_entry='date', validity='yes')

        # exit -----------------
        labelExit = self.labels(self.frameInputsCashDay, 'Saida:', 0.36, 0.64, width=0.16, color='#803356')
        self.exitDayEntry = self.entry(self.frameInputsCashDay, 0.47, 0.64, 0.2, 0.12, type_entry='entry')

        # metody exit -----------------
        labelMetodyExit = self.labels(self.frameInputsCashDay, 'M/Saída:', 0.36, 0.78, width=0.16, color='#803356')
        self.MetodyExitDayEntry = self.entry(
            self.frameInputsCashDay, 0.47, 0.78, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # events bind ===================================
        labelCustom.bind('<Double-Button-1>', lambda e: self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', '', self.dateDayEntry.get(), ''], type_search='resumeForCash', save_seacrh=False))
        labelProduty.bind('<Double-Button-1>', lambda e: self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', '', self.dateDayEntry.get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash'))
        labelCard.bind('<Double-Button-1>', lambda e: [
            self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', labelCard.cget('text'), self.dateDayEntry.get(), ''], type_search='resumeForCash', save_seacrh=False),
            self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', labelCard.cget('text'), self.dateDayEntry.get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')
        ])
        labelMoney.bind('<Double-Button-1>', lambda e: [
            self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', labelMoney.cget('text'), self.dateDayEntry.get(), ''], type_search='resumeForCash', save_seacrh=False),
            self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', labelMoney.cget('text'), self.dateDayEntry.get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')
        ])
        labelTransfer.bind('<Double-Button-1>', lambda e: [
            self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', labelTransfer.cget('text'), self.dateDayEntry.get(), ''], type_search='resumeForCash', save_seacrh=False),
            self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', labelTransfer.cget('text'), self.dateDayEntry.get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')
        ])
        labelNote.bind('<Double-Button-1>', lambda e: [
            self.search_schedule(self.treeviewCashDaySchedules, ['', '', '', '', labelNote.cget('text'), self.dateDayEntry.get(), ''], type_search='resumeForCash', save_seacrh=False),
            self.search_stock(self.treeviewCashDayProducts, ['', '', '', '', '', '', labelNote.cget('text'), self.dateDayEntry.get()], typeStock='productSaleSold', sqlSearch=searchSoldStockResumeForCash, save_seacrh=False, type_search='resumeForCash')
        ])
        self.dateDayEntry.bind('<<DateEntrySelected>>', lambda e: [
            self.pick_informations_for_cash(entryPicker()[1], self.dateDayEntry.get(), 'day'),
            self.search_cashManagement(
                self.treeviewCashDayInformations,
                entryPicker()[2],
                parameters={
                    'typeDate': 'data',
                    'table': 'Gerenciamento_do_dia',
                    'type_cash': 'cashDay'
                }
            )
        ])

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashDay, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDaySchedules, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashDay, '', 0.05, 0.87, 0.04, 0.10,
            function=lambda: self.pick_informations_for_cash(entryPicker()[1], self.dateDayEntry.get(), 'day'),
            photo=self.image('assets/icon_cashFlow.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashDay, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: [
                self.delete_informations_treeview(self.treeviewCashDayInformations, self.lineTreeviewColor['cashDay']),
                self.delete_informations_treeview(self.treeviewCashDaySchedules, self.lineTreeviewColor['cashDaySchedules']),
                self.delete_informations_treeview(self.treeviewCashDayProducts, self.lineTreeviewColor['cashDayProducts']),
            ],
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewCashDaySchedules = self.frame(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.005, 0.45, 0.422, 0.53)
        self.frameTreeviewCashDayProducts = self.frame(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.005, 0.01, 0.293, 0.43)
        self.frameTreeviewCashDayInformations = self.frame(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.43, 0.45, 0.57, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTableInformations = ('ID', 'T/Clientes', 'T/Produtos', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'T/Permuta', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'S/Permuta', 'Caixa', 'T/Recebido', 'Data')
        informationOfTableSchedule = ('Cliente', 'Serviço', 'Valor', 'Método de Pagamento', 'Profissional', 'Data', 'Horário', 'Data de Pagamento')
        informationOfTableProducts = ('Fornecedor', 'Marca', 'Tipo', 'Quantidade', 'Medida', 'V/venda', 'Cliente', 'Método de Pagamento', 'Venda')
        self.treeviewCashDayProducts = self.treeview(self.frameTreeviewCashDayProducts, informationOfTableProducts, max_width=200)
        self.treeviewCashDaySchedules = self.treeview(self.frameTreeviewCashDaySchedules, informationOfTableSchedule, max_width=150)
        self.treeviewCashDayInformations = self.treeview(self.frameTreeviewCashDayInformations, informationOfTableInformations)
        self.lineTreeviewColor['cashDay'] = 0
        self.lineTreeviewColor['cashDaySchedules'] = 0
        self.lineTreeviewColor['cashDayProducts'] = 0
        # event bind treeview ==========================================
        self.treeviewCashDayInformations.bind(
            "<Double-Button-1>", lambda e: [
                self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDayInformations, type_insert='advanced', table='Gerenciamento_do_dia', data_base='cash'),
                self.search_informations_of_cash(self.treeviewCashDayInformations, 'day')
            ]
        )

        # save last search schedule ===================================
        self.lastSearch['cashDay'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_cashManagement(
                entryPicker()[0],
                self.treeviewCashDayInformations,
                button=deleteInformationsInputs,
                parameters={
                    'sqlRegister': registerCashManagement,
                    'typeDate': 'data',
                    'table': 'Gerenciamento_do_dia',
                    'type_cash': 'cashDay'
                }
            ),
            'search': lambda: self.search_cashManagement(
                self.treeviewCashDayInformations,
                entryPicker()[0],
                parameters={
                    'typeDate': 'data',
                    'table': 'Gerenciamento_do_dia',
                    'type_cash': 'cashDay'
                }
            ),
            'order': lambda e: self.search_cashManagement(
                self.treeviewCashDayInformations,
                entryPicker()[0],
                parameters={
                    'typeDate': 'data',
                    'table': 'Gerenciamento_do_dia',
                    'type_cash': 'cashDay'
                }
            ),
            'update': lambda: self.update_cashManagement(
                self.treeviewCashDayInformations,
                entryPicker()[0],
                parameters={
                    'typeDate': 'data',
                    'table': 'Gerenciamento_do_dia',
                    'type_cash': 'cashDay',
                    'sqlUpdate': updateCashManagement
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement,
                parameter={
                    'treeview': self.treeviewCashDayInformations,
                    'parameters': {
                        'typeDate': 'data',
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                    }
                }
            ),
            'pdf': lambda: self.create_pdf_cashManagement(
                self.treeviewCashDayInformations,
                parameters={
                    'typeDate': 'data',
                    'table': 'Gerenciamento_do_dia',
                    'type_cash': 'cashDay',
                    'type_message': 'Dias',
                    'tablePart1': tableWithInformationsCashManagementTreeview1,
                    'tablePart2': tableWithInformationsCashManagementTreeview2,
                    'supplementaryTable': tableWithInformationsComplementaryCashManagement
                }
            ),
            'informations': lambda: self.message_informations_cashManagement(
                self.treeviewCashDayInformations,
                parameters={
                    'type_message': 'Dias'
                }
            ),
            'close': lambda: self.close_cash(self.treeviewCashDayInformations, parameters={'close': 'DIA FINALIZADO', 'table': 'Gerenciamento_do_dia', 'type_cash': 'cashDay'}, button=deleteInformationsInputs, button2=clear)
        }
        self.orderBtnDay = self.tab_of_buttons(0.69, 0.02, 0.28, 0.9, self.frameInputsCashDay, functions, self.photosAndIcons, informationOfTableInformations, type_btns='close', type_register='Iniciar dia')
        self.orderBtnDay.set('Data')

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashDay.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # order =============================================
            entrysGet.append(self.orderBtnDay.get())
            return [entrysGet, entrys, ['', '', '', '', '', '', '', '', '', self.dateDayEntry.get(), '', '', self.orderBtnDay.get()]]

        # init search =============================
        self.search_cashManagement(
            self.treeviewCashDayInformations,
            entryPicker()[0],
            parameters={
                'typeDate': 'data',
                'table': 'Gerenciamento_do_dia',
                'type_cash': 'cashDay'
            }
        )
        self.pick_informations_for_cash(entryPicker()[1], self.dateDayEntry.get(), 'day')

    def frame_cash_register_management_month(self):
        # frame inputs ==========================================
        self.frameInputsCashMonth = self.frame(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.30, 0.01, 0.70, 0.43)

        # observation --------------------
        self.observationCashMonthEntry = self.text_box(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.005, 0.01, 0.13, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashMonth, 'T/Clientes:', 0.02, 0.08, width=0.12)
        self.customMonthEntry = self.entry(self.frameInputsCashMonth, 0.16, 0.08, 0.18, 0.12, type_entry='entry')

        # produty -------------
        labelProduty = self.labels(self.frameInputsCashMonth, 'T/Produtos:', 0.02, 0.22, width=0.15)
        self.productMonthEntry = self.entry(self.frameInputsCashMonth, 0.16, 0.22, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashMonth, 'T/Cartão:', 0.02, 0.36, width=0.15)
        self.cardMonthEntry = self.entry(self.frameInputsCashMonth, 0.16, 0.36, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashMonth, 'T/Dinheiro:', 0.02, 0.50, width=0.15)
        self.moneyMonthEntry = self.entry(self.frameInputsCashMonth, 0.16, 0.50, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashMonth, 'T/Transferência:', 0.02, 0.64, width=0.18)
        self.transferMonthEntry = self.entry(self.frameInputsCashMonth, 0.21, 0.64, 0.13, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashMonth, 'T/Nota:', 0.02, 0.78, width=0.16)
        self.noteMonthEntry = self.entry(self.frameInputsCashMonth, 0.16, 0.78, 0.18, 0.12, type_entry='entry')

        # Permute -------------
        labelPermute = self.labels(self.frameInputsCashMonth, 'T/Permuta:', 0.36, 0.08, width=0.16)
        self.permuteDayEntry = self.entry(self.frameInputsCashMonth, 0.485, 0.08, 0.175, 0.12, type_entry='entry')

        # total exit -----------------
        labelToReceive = self.labels(self.frameInputsCashMonth, 'Caixa:', 0.36, 0.22, width=0.16)
        self.toReceiveMonthEntry = self.entry(self.frameInputsCashMonth, 0.47, 0.22, 0.19, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashMonth, 'T/Recebido:', 0.36, 0.36, width=0.16)
        self.receivedMonthEntry = self.entry(self.frameInputsCashMonth, 0.495, 0.36, 0.165, 0.12, type_entry='entry')

        # month -----------------
        labelMonth = self.labels(self.frameInputsCashMonth, 'Mês:', 0.36, 0.50, width=0.16)
        self.dateMonthEntry = self.entry(self.frameInputsCashMonth, 0.47, 0.50, 0.14, 0.12, type_entry='date', validity='yes')
        self.dateMonthEntry.delete(0, END)
        self.dateMonthEntry.insert(0, datetime.today().strftime("%m/%Y"))

        # exit -----------------
        labelExit = self.labels(self.frameInputsCashMonth, 'Saida:', 0.36, 0.64, width=0.16, color='#803356')
        self.exitMonthEntry = self.entry(self.frameInputsCashMonth, 0.47, 0.64, 0.2, 0.12, type_entry='entry')

        # metody exit -----------------
        labelMetodyExit = self.labels(self.frameInputsCashMonth, 'M/Saida:', 0.36, 0.78, width=0.16, color='#803356')
        self.metodyExitMonthEntry = self.entry(
            self.frameInputsCashMonth, 0.47, 0.78, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'PERMUTA']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashMonth, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashMonth, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashMonth, '', 0.05, 0.87, 0.04, 0.10,
            function=lambda: [
                self.password_window(self.pick_informations_for_cash, {'entrys': entryPicker()[1], 'date': self.dateMonthEntry.get(), 'type': 'month'}),
                self.search_informations_of_cash(self.treeviewCashMonth, 'month')
            ],
            photo=self.image('assets/icon_cashFlow.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashMonth, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: [
                self.delete_informations_treeview(self.treeviewCashMonth, self.lineTreeviewColor['cashMonth']),
                self.delete_informations_treeview(self.treeviewCashMonthDay, self.lineTreeviewColor['cashMonthDays'])
            ],
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frame inputs ========================
        self.dateMonthEntry.bind(
            '<<DateEntrySelected>>',
            lambda e: self.dateMonthEntry.delete(0, 3)
        )
        self.dateMonthEntry.bind('<FocusOut>', lambda e: self.dateMonthEntry.delete(0, 3) if len(self.dateMonthEntry.get()) > 7 else '')

        # frame treeview ==================
        self.frameTreeviewCashMonthDays = self.frame(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.005, 0.01, 0.293, 0.43)
        self.frameTreeviewCashMonth = self.frame(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'T/Clientes', 'T/Produtos', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'T/Permuta', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'S/Permuta', 'Caixa', 'T/Recebido', 'Mês')
        informationOfTableDays = ('ID', 'T/Clientes', 'T/Produtos', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'T/Permuta', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'S/Permuta', 'Caixa', 'T/Recebido', 'Data')
        self.treeviewCashMonth = self.treeview(self.frameTreeviewCashMonth, informationOfTable)
        self.treeviewCashMonthDay = self.treeview(self.frameTreeviewCashMonthDays, informationOfTableDays)
        self.lineTreeviewColor['cashMonth'] = 0
        self.lineTreeviewColor['cashMonthDays'] = 0
        # event bind treeview ==========================================
        self.treeviewCashMonth.bind(
            "<Double-Button-1>", lambda e: [
                self.insert_informations_entrys(entryPicker()[1], self.treeviewCashMonth, type_insert='advanced', table='Gerenciamento_do_mês', data_base='cash'),
                self.search_informations_of_cash(self.treeviewCashMonth, 'month')
            ]
        )

        # save last search schedule ===================================
        self.lastSearch['cashMonth'] = ''

        functions = {
            'register': lambda: self.password_window(
                self.register_cashManagement, {
                    'informations': entryPicker()[0],
                    'treeview': self.treeviewCashMonth,
                    'button': deleteInformationsInputs,
                    'parameters': {
                        'sqlRegister': registerCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    },
                }
            ),
            'search': lambda: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    },
                }
            ),
            'order': lambda e: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    },
                }
            ),
            'update': lambda: self.password_window(
                self.update_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateCashManagement,
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'pdf': lambda: self.password_window(
                self.create_pdf_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'tablePart1': tableWithInformationsCashManagementTreeview1,
                        'tablePart2': tableWithInformationsCashManagementTreeview2,
                        'supplementaryTable': tableWithInformationsComplementaryCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês',
                        'type_message': 'Meses'
                    }
                }
            ),
            'informations': lambda: self.password_window(
                self.message_informations_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'type_message': 'Meses'
                    }
                }
            ),
            'close': lambda: self.password_window(
                self.close_cash, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'close': 'MÊS FINALIZADO',
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth'
                    },
                    'button': deleteInformationsInputs
                }
            )
        }
        self.orderBtnMonth = self.tab_of_buttons(0.69, 0.02, 0.28, 0.9, self.frameInputsCashMonth, functions, self.photosAndIcons, informationOfTable, type_btns='close', type_register='Iniciar mês', type_close='Fechar mês')

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashMonth.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # order =============================================
            entrysGet.append(self.orderBtnMonth.get())
            return [entrysGet, entrys]

        self.search_cashManagement(
            self.treeviewCashMonth,
            ['', '', '', '', '', '', '', '', '', self.dateMonthEntry, '', '', 'mês'],
            parameters={
                'sqlSearch': searchCashManagement,
                'table': 'Gerenciamento_do_mês',
                'type_cash': 'cashMonth',
                'typeDate': 'mês'
            },
            insert=False)

    def frame_cash_register_management_general(self):

        # frame inputs ==========================================
        self.frameInputsCashGeneral = self.frame(self.typeCashManagement.tab(' Gerenciamento geral '), 0.005, 0.01, 0.989, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashGeneral, 'T/Cliente:', 0.02, 0.08, width=0.12)
        self.customDayEntry = self.entry(self.frameInputsCashGeneral, 0.16, 0.08, 0.18, 0.12, type_entry='entry')

        # produty -------------
        labelProduty = self.labels(self.frameInputsCashGeneral, 'T/Produto:', 0.02, 0.22, width=0.15)
        self.productDayEntry = self.entry(self.frameInputsCashGeneral, 0.16, 0.22, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashGeneral, 'T/Cartão:', 0.02, 0.36, width=0.15)
        self.cardDayEntry = self.entry(self.frameInputsCashGeneral, 0.16, 0.36, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashGeneral, 'T/Dinheiro:', 0.02, 0.50, width=0.15)
        self.moneyDayEntry = self.entry(self.frameInputsCashGeneral, 0.16, 0.50, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashGeneral, 'T/Transferência:', 0.02, 0.64, width=0.18)
        self.transferDayEntry = self.entry(self.frameInputsCashGeneral, 0.21, 0.64, 0.13, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashGeneral, 'T/Nota:', 0.02, 0.78, width=0.16)
        self.noteDayEntry = self.entry(self.frameInputsCashGeneral, 0.16, 0.78, 0.18, 0.12, type_entry='entry')

        # Permute -------------
        labelPermute = self.labels(self.frameInputsCashGeneral, 'T/Permuta:', 0.36, 0.08, width=0.16)
        self.permuteDayEntry = self.entry(self.frameInputsCashGeneral, 0.485, 0.08, 0.175, 0.12, type_entry='entry')

        # to receive -----------------
        labelCash = self.labels(self.frameInputsCashGeneral, 'F/Caixa:', 0.36, 0.22, width=0.16)
        self.CashDayEntry = self.entry(self.frameInputsCashGeneral, 0.47, 0.22, 0.19, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashGeneral, 'T/Recebido:', 0.36, 0.36, width=0.16)
        self.receivedDayEntry = self.entry(self.frameInputsCashGeneral, 0.495, 0.36, 0.165, 0.12, type_entry='entry')

        # date -----------------
        labelDate = self.labels(self.frameInputsCashGeneral, 'Data:', 0.36, 0.50, width=0.16)
        self.dateDayInitEntry = self.entry(self.frameInputsCashGeneral, 0.47, 0.50, 0.14, 0.12, type_entry='date', validity='yes')
        labelDate = self.labels(self.frameInputsCashGeneral, 'até', 0.52, 0.65, width=0.16)
        self.dateDayFinishEntry = self.entry(self.frameInputsCashGeneral, 0.47, 0.78, 0.14, 0.12, type_entry='date', validity='yes')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashGeneral, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDaySchedules, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashGeneral, '', 0.05, 0.87, 0.04, 0.10,
            function=lambda: self.password_window(
                self.pick_informations_for_cashGeneral,
                parameter={
                    'entrys': entryPicker()[1]
                }
            ),
            photo=self.image('assets/icon_cashFlow.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashGeneral, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: [
                self.delete_informations_treeview(self.treeviewCashDayGeneral, self.lineTreeviewColor['cashGeneral']),
            ],
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewCashDayInformations = self.frame(self.typeCashManagement.tab(' Gerenciamento geral '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTableInformations = ('ID', 'T/Clientes', 'T/Produtos', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'T/Permuta', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'S/Permuta', 'Caixa', 'T/Recebido', 'Período', 'Data')

        self.treeviewCashDayGeneral = self.treeview(self.frameTreeviewCashDayInformations, informationOfTableInformations)
        self.lineTreeviewColor['cashGeneral'] = 0
        # event bind treeview ==========================================
        self.treeviewCashDayGeneral.bind(
            "<Double-Button-1>", lambda e: [
                self.insert_inputs_generalCash(self.treeviewCashDayGeneral, entryPicker()[1]),
                self.search_informations_of_cash(self.treeviewCashDayGeneral, 'day')
            ]
        )
        # save last search schedule ===================================
        self.lastSearch['cashGeneral'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(
                self.register_cashManagement, {
                    'informations': entryPicker()[0],
                    'treeview': self.treeviewCashDayGeneral,
                    'button': deleteInformationsInputs,
                    'parameters': {
                        'sqlRegister': registerCashManagementGeneral,
                        'table': 'Gerenciamento_geral',
                        'type_cash': 'cashGeneral',
                        'typeDate': 'General'
                    },
                }
            ),
            'search': lambda: self.password_window(
                self.search_cashManagementGeneral, {
                    'treeview': self.treeviewCashDayGeneral,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'table': 'Gerenciamento_geral',
                        'type_cash': 'cashGeneral',
                    },
                }
            ),
            'order': lambda e: self.password_window(
                self.search_cashManagementGeneral, {
                    'treeview': self.treeviewCashDayGeneral,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'table': 'Gerenciamento_geral',
                        'type_cash': 'cashGeneral',
                    },
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement,
                parameter={
                    'treeview': self.treeviewCashDayGeneral,
                    'parameters': {
                        'typeDate': 'data',
                        'table': 'Gerenciamento_geral',
                        'type_cash': 'cashGeneral',
                    }
                }
            ),
            'pdf': lambda: self.password_window(
                self.create_pdf_cashManagement, {
                    'treeview': self.treeviewCashDayGeneral,
                    'parameters': {
                        'table': 'Gerenciamento_geral',
                        'type_cash': 'cashGeneral',
                        'type_message': 'Dias',
                        'tablePart1': tableWithInformationsCashManagementGeneralTreeview1,
                        'tablePart2': tableWithInformationsCashManagementGeneralTreeview2,
                        'supplementaryTable': tableWithInformationsComplementaryCashManagementGeneral
                    },
                    'type_pdf': 'general'
                }
            ),
            'informations': lambda: self.password_window(
                self.message_informations_cashManagement, {
                    'treeview': self.treeviewCashDayGeneral,
                    'parameter': None,
                    'type_msn': 'general'
                }
            )
        }
        self.orderBtnGeneral = self.tab_of_buttons(0.69, 0.02, 0.28, 0.9, self.frameInputsCashGeneral, functions, self.photosAndIcons, informationOfTableInformations, type_btns='managementGeneral')
        self.orderBtnGeneral.set('Data')

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashGeneral.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # order =============================================
            entrysGet.append(self.orderBtnGeneral.get())
            return [entrysGet, entrys]

    def frame_pay_management(self):
        # frame inputs ==========================================
        self.frameInputsCashPay = self.frame(self.employersPayFrame, 0.14, 0.01, 0.855, 0.43)

        # observation --------------------
        self.observationCashPayEntry = self.text_box(self.employersPayFrame, 0.005, 0.01, 0.13, 0.43)

        # employee -------------
        labelEmployee = self.labels(self.frameInputsCashPay, 'Profissional:', 0.02, 0.22, width=0.12)
        self.employeeCashPayEntry = self.entry(
            self.frameInputsCashPay, 0.14, 0.22, 0.18, 0.12, type_entry='list'
        )

        # Date -------------
        labelMonth = self.labels(self.frameInputsCashPay, 'Data:', 0.02, 0.36, width=0.15)
        self.dayInitCashPayEntry = self.entry(self.frameInputsCashPay, 0.09, 0.36, 0.10, 0.12, type_entry='date', validity='yes')
        labelDate = self.labels(self.frameInputsCashPay, 'até', 0.197, 0.37, width=0.10)
        self.dayFinishCashPayEntry = self.entry(self.frameInputsCashPay, 0.23, 0.36, 0.10, 0.12, type_entry='date', validity='yes')

        # custom -------------
        labelCustom = self.labels(self.frameInputsCashPay, 'T/Clientes:', 0.02, 0.50, width=0.15)
        self.customCashPayEntry = self.entry(self.frameInputsCashPay, 0.14, 0.50, 0.18, 0.12, type_entry='entry')

        # invoicing -------------
        labelInvoicing = self.labels(self.frameInputsCashPay, 'Faturamento:', 0.02, 0.64, width=0.15)
        self.invoicingCashPayEntry = self.entry(self.frameInputsCashPay, 0.15, 0.64, 0.17, 0.12, type_entry='entry')

        # percentage -------------
        labelPercentage = self.labels(self.frameInputsCashPay, 'Porcentagem:', 0.34, 0.22, width=0.15)
        self.percentageCashPayEntry = self.entry(self.frameInputsCashPay, 0.47, 0.22, 0.17, 0.12, type_entry='entry')

        # payment -------------
        labelPayment = self.labels(self.frameInputsCashPay, 'Pagamento:', 0.34, 0.36, width=0.16)
        self.paymentCashPayEntry = self.entry(self.frameInputsCashPay, 0.47, 0.36, 0.17, 0.12, type_entry='entry')

        # method paymant -----------------
        labelMethodPayment = self.labels(self.frameInputsCashPay, 'M/Pagamento:', 0.34, 0.50, width=0.16)
        self.metohPaymentCashPayEntry = self.entry(
            self.frameInputsCashPay, 0.47, 0.50, 0.17, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # method paymant -----------------
        labelMethodPaymentSearch = self.labels(self.frameInputsCashPay, 'BM/Pagamento:', 0.34, 0.64, width=0.16)
        self.metohPaymentCashPaySearchEntry = self.entry(
            self.frameInputsCashPay, 0.49, 0.64, 0.15, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashPay, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashPayment, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashPay, '', 0.05, 0.87, 0.04, 0.10,
            function=lambda: self.password_window(
                self.pick_informations_for_payment, {
                    "entrys": entryPicker()[1],
                    "date": [self.dayInitCashPayEntry.get(), self.dayFinishCashPayEntry.get()],
                    "profissional": self.employeeCashPayEntry.get(),
                    "method": self.metohPaymentCashPaySearchEntry.get()
                }
            ),
            photo=self.image('assets/icon_cashFlow.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashPay, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: self.delete_informations_treeview(self.treeviewCashPayment, self.lineTreeviewColor['cashPayment']),
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        self.percentageCashPayEntry.bind(
            '<FocusOut>',
            lambda e: [
                self.paymentCashPayEntry.delete(0, END),
                self.paymentCashPayEntry.insert(0, self.calculing_percentage_for_payment(self.invoicingCashPayEntry.get(), self.percentageCashPayEntry.get()))
            ]
        )
        self.employeeCashPayEntry.bind('<KeyPress>', lambda e: self.employeeCashPayEntry.configure(
            values=[name[1] for name in self.search_professional(informations=self.searching_list(self.employeeCashPayEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))

        # frame treeview ==================
        self.frameTreeviewCashPay = self.frame(self.employersPayFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Profissional', 'Mês de pagamento', 'T/Clientes', 'Faturamento', 'Porcentagem', 'Pagamento', 'Método de pagamento', 'Data de pagamento')
        self.treeviewCashPayment = self.treeview(self.frameTreeviewCashPay, informationOfTable)
        self.lineTreeviewColor['cashPayment'] = 0
        # event bind treeview ==========================================
        self.treeviewCashPayment.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashPayment, type_insert='advanced', table='Gerenciador_de_pagamentos', data_base='cash')
        )

        # save last search schedule ===================================
        self.lastSearch['cashPayment'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(self.register_payment, {'informationa': entryPicker()[0], 'treeviw': self.treeviewCashPayment}),
            'search': lambda: self.password_window(self.search_payment, {'treeview': self.treeviewCashPayment, 'informations': entryPicker()[0]}),
            'order': lambda e: self.password_window(self.search_payment, {'treeview': self.treeviewCashPayment, 'informations': entryPicker()[0]}),
            'update': lambda: self.password_window(self.update_payment, {'treeview': self.treeviewCashPayment, 'informations': entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_payment, {'treeview': self.treeviewCashPayment}),
            'pdf': lambda: self.password_window(self.create_pdf_payment, {'treeview': self.treeviewCashPayment}),
            'informations': lambda: self.password_window(self.message_informations_payment, {'treeview': self.treeviewCashPayment})
        }
        self.orderBtnPay = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsCashPay, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashPay.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # observations informations ====================
            entrysGet.append(self.observationCashPayEntry.get("1.0", "end-1c"))
            entrys.append(self.observationCashPayEntry)

            # order =============================================
            entrysGet.append(self.orderBtnPay.get())
            return [entrysGet, entrys]

        # init search ===========================================
        self.search_payment(self.treeviewCashPayment, self.searching_list('', 7, 'ID'), insert=False)


if __name__ == '__main__':
    app = Aplication()
