from tkinter import ttk
from tkinter import *
from tkcalendar import *
from customtkinter import *


class Interface:
    @staticmethod
    def labels(window, text, posx, posy, width=0.1, height=0.1, color='black', background='white', position=W, photo=None, size=21, font='Arial'):
        label = CTkLabel(window, text=text, font=CTkFont(font, size, 'bold'), fg_color=background, anchor=position, text_color=color, image=photo)
        label.place(relx=posx, rely=posy, relwidth=width, relheight=height)
        return label

    @staticmethod
    def entry(
            window, posx, posy, width=0.1, height=0.1, value=None, type_entry='list', place_text='', position=LEFT, validity='no', function=None, background='#FFFFFF',
            radius=20, border=0, show=''
    ):
        if value is None:
            value = []
        camp = None
        match type_entry:
            case 'list':
                camp = CTkComboBox(
                    window, fg_color='#FFFFFF', text_color='black', border_color='#f25298', values=value, dropdown_fg_color='white', dropdown_hover_color='#f25298',
                    button_color='pink', button_hover_color='#f25298', font=CTkFont('Arial', 16), dropdown_text_color='black', command=function
                )
                camp.place(relx=posx, rely=posy, relwidth=width, relheight=height)
                camp.set('')
            case 'entry':
                camp = CTkEntry(
                    window, fg_color='#FFFFFF', text_color='#000000', border_color='#f25298',  font=CTkFont('Arial', 16), placeholder_text=place_text,
                    placeholder_text_color='#222222', justify=position, show=show
                )
                camp.place(relx=posx, rely=posy, relwidth=width, relheight=height)
            case 'date':
                camp = DateEntry(
                    window, width=12, font='Arial', background='#fff', fg='black', locale='pt_BR', headersbackground='pink', headersforeground='#e8257a',
                    foreground='#e8257a', highlightthickness=7, highlightcolor='black'
                )

                if validity == 'no':
                    camp.config(validate='none')
                    camp.delete(0, END)

                camp.place(relx=posx, rely=posy, relwidth=width, relheight=height)
            case 'entryLogin':
                camp = CTkEntry(
                    window, fg_color=background, text_color='#000000', border_color='#f25298', font=CTkFont('Arial', 16), placeholder_text=place_text,
                    placeholder_text_color='#222222', justify=position, corner_radius=radius, border_width=border, show=show
                )
                camp.place(relx=posx, rely=posy, relwidth=width, relheight=height)
        return camp

    @staticmethod
    def button(
            window, text, posx, posy,  width=None, height=None, function=None, type_btn='normal', order_list=None, photo=None, background='#b31d5e', retur_variable=None, value='', hover_cursor='#b5517d',
            border=2, color='#ffffff'
    ):
        btn = None
        match type_btn:
            case 'normal':
                btn = CTkButton(
                    window, text=text, font=CTkFont('Arial', 17, 'bold'), command=function, image=photo,
                    fg_color=background, text_color=color, border_width=border, border_color='#f25298', hover_color='#b5517d',
                    cursor='hand2'
                )
                btn.place(relx=posx, rely=posy, relwidth=width, relheight=height)
            case 'buttonPhoto':
                btn = CTkButton(window, command=function, image=photo, fg_color='transparent', cursor='hand2', text='', hover_color=hover_cursor, corner_radius=0)
                btn.place(relx=posx, rely=posy, relwidth=width, relheight=height)
            case 'optionMenu':
                btn = CTkOptionMenu(
                    window, font=CTkFont('Arial', 17, 'bold'), command=function, values=order_list,
                    fg_color='#f584b5', button_color='#b31d5e', text_color='white', dropdown_fg_color='#b31d5e'
                )
                btn.place(relx=posx, rely=posy, relwidth=width, relheight=height)
            case 'radioButton':
                btn = CTkRadioButton(
                    window, text=text, variable=retur_variable, value=value, text_color='black', border_color='#f25298',
                    font=CTkFont('Arial', 16, 'bold'), hover_color='#b5517d', fg_color='#f25298'
                )
                btn.place(relx=posx, rely=posy, relwidth=width, relheight=height)
        return btn

    @staticmethod
    def frame(window, posx, posy,  width=None, height=None, background_color='white', border=2, radius=5):
        frm = CTkFrame(window, fg_color=background_color, border_color='#f25298', border_width=border, corner_radius=radius)
        frm.place(relx=posx, rely=posy, relwidth=width, relheight=height)
        return frm

    @staticmethod
    def notebook(locate, posx=0, posy=0.01, width=1, height=1):
        tab = ttk.Notebook(locate)
        tab.place(relx=0, rely=0.01, relwidth=1, relheight=1)
        return tab

    @staticmethod
    def main_frame_notebook(locate, name_tab, bg='white'):
        frame = Frame(locate, background=bg)
        frame.place(relx=0, rely=0.01, relwidth=1, relheight=1)
        locate.add(frame, text=name_tab, padding=[5, 0])
        return frame

    @staticmethod
    def tabvieew(locate, posx, posy, width, height, background='pink', border='#f25298'):
        tab = CTkTabview(
            locate, fg_color=background, border_width=3, border_color=border, segmented_button_fg_color='#f25298', segmented_button_unselected_color='#f25298',
            text_color='white', segmented_button_selected_color='#b36684', segmented_button_unselected_hover_color='#f786b7', segmented_button_selected_hover_color='#f786b7'
        )
        tab.place(relx=posx, rely=posy, relwidth=width, relheight=height)
        return tab

    @staticmethod
    def scrollbar(locate, orient, position, x_or_y):
        scrollbar = CTkScrollbar(
            locate, orientation=orient, button_color='#f598c0', minimum_pixel_length=200, fg_color='#d8d8d8', border_spacing=1,
            button_hover_color='#f7599d'
        )
        scrollbar.pack(side=position, fill=x_or_y)
        return scrollbar

    def treeview(self, locate, informations, max_width=0):
        # scrollbar ---------------------------------------------------
        yscrollbar = self.scrollbar(locate, 'vertical', RIGHT, Y)
        xscrollbar = self.scrollbar(locate, 'horizontal', BOTTOM, X)

        # Treeview -----------------------------------------------------
        treeview = ttk.Treeview(locate, columns=informations, show='headings', height=24, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        yscrollbar.configure(command=treeview.yview)
        xscrollbar.configure(command=treeview.xview)

        # configurando
        for name in informations:
            if max_width > 0:
                treeview.column(f'{name}', minwidth=20, width=max_width, anchor=W, stretch=False)
            elif name == 'ID':
                treeview.column(f'{name}', minwidth=20, width=50, anchor=W, stretch=False)
            elif name in ['Valor', 'Data', 'Horário', 'Caixa']:
                treeview.column(f'{name}', minwidth=20, width=100, anchor=W, stretch=False)
            elif name in ['Agendamento', 'Método de Pagamento']:
                treeview.column(f'{name}', minwidth=20, width=150, anchor=W, stretch=False)
            elif name in ['Cliente', 'Serviço', 'Profissional', 'Nome']:
                treeview.column(f'{name}', minwidth=20, width=300, anchor=W, stretch=False)
            elif 'T/' in name or 'S/' in name:
                treeview.column(f'{name}', minwidth=20, width=100, anchor=W, stretch=False)
            else:
                treeview.column(f'{name}', minwidth=20, width=250, anchor=W, stretch=False)
        for names in informations:
            treeview.heading(f'{names}', text=f'{names}', anchor=W)
        treeview.tag_configure('oddrow', background='pink')
        treeview.tag_configure('evenrow', background='#ffe8f1')
        treeview.place(relx=0.002, rely=0.01, relwidth=0.985, relheight=0.95)
        return treeview

    @staticmethod
    def text_box(locate, posx, posy, width, height):
        textBox = CTkTextbox(
            locate, border_width=2, border_color='#f25298', fg_color='white', text_color='black', font=CTkFont('Arial', 14),
            scrollbar_button_color='#f598c0', scrollbar_button_hover_color='#f7599d'
        )
        textBox.place(relx=posx, rely=posy, relwidth=width, relheight=height)
        return textBox

    def tab_of_buttons(self, posx, posy, width, height, locate, functions, icons, values=None, treeview='yes', type_btns='complete', type_register='Cadastrar', type_close='Fechar Dia'):
        # buttons management ============
        frameBtns = self.tabvieew(locate, posx, posy, width, height)
        frameBtns.add('Gerenciamento')

        if type_btns == 'complete':
            # registration ----------
            registrationBtn = self.button(frameBtns.tab('Gerenciamento'), type_register, 0.225, 0.00, 0.55, 0.2, function=functions['register'])
            # search -------------
            searchBtn = self.button(frameBtns.tab('Gerenciamento'), 'Buscar', 0.225, 0.25, 0.55, 0.2, function=functions['search'])
            # update -------------
            updateBtn = self.button(frameBtns.tab('Gerenciamento'), 'Atualizar', 0.225, 0.50, 0.55, 0.2, function=functions['update'])
            # delete ---------
            deleteBtn = self.button(frameBtns.tab('Gerenciamento'), 'Deletar', 0.225, 0.75, 0.55, 0.2, function=functions['delete'])
        elif type_btns == 'sale':
            # registration ----------
            registrationBtn = self.button(frameBtns.tab('Gerenciamento'), 'Cadastrar', 0.225, 0.00, 0.55, 0.17, function=functions['register'])
            # search -------------
            searchBtn = self.button(frameBtns.tab('Gerenciamento'), 'Buscar', 0.225, 0.20, 0.55, 0.17, function=functions['search'])
            # update -------------
            updateBtn = self.button(frameBtns.tab('Gerenciamento'), 'Atualizar', 0.225, 0.40, 0.55, 0.17, function=functions['update'])
            # sale ---------
            saleBtn = self.button(frameBtns.tab('Gerenciamento'), 'Venda', 0.225, 0.60, 0.55, 0.17, function=functions['sale'])
            # delete
            deleteBtn = self.button(frameBtns.tab('Gerenciamento'), 'Deletar', 0.225, 0.80, 0.55, 0.17, function=functions['delete'])
        elif type_btns == 'close':
            # registration ----------
            registrationBtn = self.button(frameBtns.tab('Gerenciamento'), type_register, 0.225, 0.00, 0.55, 0.17, function=functions['register'])
            # search -------------
            searchBtn = self.button(frameBtns.tab('Gerenciamento'), 'Buscar', 0.225, 0.20, 0.55, 0.17, function=functions['search'])
            # update -------------
            updateBtn = self.button(frameBtns.tab('Gerenciamento'), 'Atualizar', 0.225, 0.40, 0.55, 0.17, function=functions['update'])
            # sale ---------
            saleBtn = self.button(frameBtns.tab('Gerenciamento'), type_close, 0.225, 0.60, 0.55, 0.17, function=functions['close'])
            # delete
            deleteBtn = self.button(frameBtns.tab('Gerenciamento'), 'Deletar', 0.225, 0.80, 0.55, 0.17, function=functions['delete'])
        elif type_btns == 'management':
            # search -------------
            searchBtn = self.button(frameBtns.tab('Gerenciamento'), 'Buscar', 0.225, 0.05, 0.55, 0.2, function=functions['search'])
            # update -------------
            updateBtn = self.button(frameBtns.tab('Gerenciamento'), 'Atualizar', 0.225, 0.36, 0.55, 0.2, function=functions['update'])
            # delete ---------
            deleteBtn = self.button(frameBtns.tab('Gerenciamento'), 'Deletar', 0.225, 0.67, 0.55, 0.2, function=functions['delete'])
        elif type_btns == 'managementGeneral':
            # search -------------
            searchBtn = self.button(frameBtns.tab('Gerenciamento'), 'Cadastrar', 0.225, 0.05, 0.55, 0.2, function=functions['register'])
            # update -------------
            updateBtn = self.button(frameBtns.tab('Gerenciamento'), 'Buscar', 0.225, 0.36, 0.55, 0.2, function=functions['search'])
            # delete ---------
            deleteBtn = self.button(frameBtns.tab('Gerenciamento'), 'Deletar', 0.225, 0.67, 0.55, 0.2, function=functions['delete'])
        if treeview == 'yes':
            # buttons treeview ================
            frameBtns.add('Tabela')
            # order --------------
            labelOrder = self.labels(frameBtns.tab('Tabela'), 'Ordem', 0.25, 0.0, width=0.50, height=0.2, color='#f25298', background='pink', position=CENTER)
            orderBtn = self.button(frameBtns.tab('Tabela'), 'Deletar', 0.225, 0.20, 0.55, 0.2, type_btn='optionMenu', function=functions['order'], order_list=values)
            # pdf and informations ----------------
            labelInfo = self.labels(frameBtns.tab('Tabela'), 'Informações', 0.17, 0.45, width=0.7, height=0.2, color='#f25298', background='pink', position=CENTER)
            pdf = self.button(frameBtns.tab('Tabela'), '', 0.3, 0.7, 0.2, photo=icons['pdf'][0], type_btn='buttonPhoto', background='pink', function=functions['pdf'])
            informacao = self.button(frameBtns.tab('Tabela'), '', 0.53, 0.7, 0.2, photo=icons['informações'][0], type_btn='buttonPhoto', background='pink', function=functions['informations'])
            return orderBtn

    def informations_simple(self, locate, type_info, informations, funcs, icons, photo):
        # frame inputs ==========================================
        frameInputsInformations = self.frame(locate, 0.195, 0.01, 0.6, 0.43)

        # info --------------------
        labelInfo = self.labels(frameInputsInformations, type_info, 0.03, 0.395, width=0.16)
        informationsEntry = self.entry(frameInputsInformations, 0.20, 0.39, 0.25, 0.12, type_entry='entry')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            frameInputsInformations, 'apagar', 0.003, 0.87, 0.06, 0.12, function=lambda: informationsEntry.delete(0, END),
            photo=photo, type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        treeviewInformationFrame = self.frame(locate, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        treeviewInformation = self.treeview(treeviewInformationFrame, informations, max_width=400)

        # buttons management ============
        orderBtnInformations = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, frameInputsInformations, funcs, icons, informations)

        return {'entry': informationsEntry, 'treeview': treeviewInformation, 'order': orderBtnInformations, 'deleteInputs': deleteInformationsInputs}
