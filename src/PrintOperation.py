# -*- coding: utf-8 -*-
"""Gtk.PrintOperation()."""

import gi

gi.require_version(namespace='Gtk', version='3.0')
gi.require_version(namespace='PangoCairo', version='1.0')

from gi.repository import Gio, Gtk, Pango, PangoCairo, Gdk
import cairo

from DataAccess import Character
from Utils import DialogExportToPdf

text = ""



class PrintOperation(Gtk.Window):

    def __init__(self, id=None):
        super().__init__()

        self.img = cairo.ImageSurface.create_from_png("assets/image/bukowski.png")

        c = Character()
        c = c.get(id)
        self.name = c.name
        text = '<span size="xx-large">Ficha do Personagem</span>\n\n'
        text = text + '<b>Nome: </b>' + c.name.capitalize() + '\n'
        text = text + '<b>Arquétipo: </b>' + c.archtype +'\n'
        text = text + '<b>Data de nascimento: </b>' + c.date_of_birth.strftime("%d/%m/%Y") + '   <b>Sexo: </b>' + c.sex + '\n'
        text = text + '<b>Altura: </b> ' + str("{:1.2f}".format(c.height)) + 'm   <b>Peso: </b>' + str("{:3.2f}".format(c.weight)) + ' <i>Kg</i>\n'
        text = text + '<b>Tipo de corpo: </b>' + c.body_type + '\n'
        text = text + '<b>Cor dos olhos: </b>' + c.eye_color +   '  <b>Cor dos cabelos:</b> ' + c.hair_color + '\n'
        text = text + '<b>Etnicidade :</b> ' + c.ethnicity + '  <b>Saúde :</b>' + c.health + '\n'
        text = text + '<b>Local: </b>' + c.local + '\n'



        # Configurando a janela principal.
        self.set_title(title='Imprimir Capivara')
        self.set_default_size(width=1366 / 2, height=768 / 2)
        self.set_position(position=Gtk.WindowPosition.CENTER)
        self.set_default_icon_from_file(filename='assets/icons/icon.png')

        # Variável auxilizar com as configurações do papel.
        #self.page_setup = self._page_setup()
        self.page_setup = self._custom_page_setup()

        # Variável para o dialogo de configuração do papel:
        self.print_settings = Gtk.PrintSettings.new()

        # Widgets.
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_border_width(border_width=12)
        self.add(widget=vbox)

        # Buffer de texto.
        self.text_buffer = Gtk.TextBuffer.new()

        # Adicionando texto renderizado ao Gtk.TextView.
        text_buffer_iter = self.text_buffer.get_end_iter()
        self.text_buffer.insert_markup(
            iter=text_buffer_iter,
            markup=text,
            len=-1,
        )

        text_view = Gtk.TextView.new_with_buffer(buffer=self.text_buffer)
        vbox.pack_start(child=text_view, expand=True, fill=True, padding=0)

        h_btn_box = Gtk.ButtonBox.new(orientation=Gtk.Orientation.HORIZONTAL)
        h_btn_box.set_spacing(spacing=6)
        vbox.pack_start(child=h_btn_box, expand=False, fill=True, padding=0)

        btn_print_dialog = Gtk.Button.new_with_label('Imprimir')
        btn_print_dialog.connect('clicked', self.open_print_dialog)
        h_btn_box.pack_start(
            child=btn_print_dialog,
            expand=False,
            fill=False,
            padding=0,
        )

        btn_open_preview = Gtk.Button.new_with_label('Visualizar')
        btn_open_preview.connect('clicked', self.open_preview)
        h_btn_box.pack_start(
            child=btn_open_preview,
            expand=False,
            fill=False,
            padding=0,
        )

        btn_page_setup_dialog = Gtk.Button.new_with_label('Configurar página')
        btn_page_setup_dialog.connect('clicked', self.open_page_setup_dialog)
        h_btn_box.pack_start(
            child=btn_page_setup_dialog,
            expand=False,
            fill=False,
            padding=0,
        )

        btn_export_pdf = Gtk.Button.new_with_label('Exportar para PDF')
        btn_export_pdf.connect('clicked', self.export_to_pdf)
        h_btn_box.pack_start(
            child=btn_export_pdf,
            expand=False,
            fill=False,
            padding=0,
        )

        self.show_all()

    def _print_operation(self):
        """Operação de impressão."""
        print_operation = Gtk.PrintOperation.new()
        print_operation.set_n_pages(1)
        # configurçaão inicial.
        print_operation.set_default_page_setup(default_page_setup=self.page_setup)
        # O que cada signal (sinal) deve realizar.
        print_operation.connect('begin-print', self.begin_print)
        print_operation.connect('draw_page', self.draw_page)
        return print_operation

    def _page_setup(self):
        """Configuração padrão para o papel."""
        # Tamanho do papel.
        paper_size = Gtk.PaperSize.new(name=Gtk.PAPER_NAME_A4)

        # Configurações da página.
        page_setup = Gtk.PageSetup.new()
        page_setup.set_paper_size_and_default_margins(size=paper_size)
        return page_setup

    def _custom_page_setup(self):
        """Configuração personalizada de papel."""
        # Tamanho do papel.
        paper_size = Gtk.PaperSize.new(name=Gtk.PAPER_NAME_A4)

        # Configurações da página.
        custom_page_setup = Gtk.PageSetup.new()
        # Personalizando a marge no topo
        custom_page_setup.set_top_margin(margin=20, unit=Gtk.Unit.MM)
        custom_page_setup.set_left_margin(margin=20, unit=Gtk.Unit.MM)
        # Orientação do papel:
        custom_page_setup.set_orientation(orientation=Gtk.PageOrientation.PORTRAIT)
        # Quando a pagina é personalizada utilizar:
        custom_page_setup.set_paper_size(size=paper_size)
        return custom_page_setup

    def begin_print(self, print_operation, context):
        """Quando a operação de impressão é iniciada."""
        # #self.img
        self.context =context
        self.add_image(self.img)

        # Posição inicial e final do texto no Gtk.TextView.
        start, stop = self.text_buffer.get_bounds()
        # Texto que está no Gtk.TextView.
        text = self.text_buffer.get_text(
            start=start,
            end=stop,
            include_hidden_chars=True,
        )
        # Contexto onde os dados serão inseridos.
        self.pango_layout = context.create_pango_layout()
        self.pango_layout.set_markup(text=text, length=-1)
        # Definindo uma configuração de fonte para a impressão.
        self.pango_layout.set_font_description(Pango.FontDescription('Courier 12'))
        self.pango_layout.set_spacing(2)

    def draw_page(self, print_operation, context, page_nr):
        """Desenhando a página."""
        # Criando o contexto.
        cairo_context = context.get_cairo_context()
        # Cor da fonte.
        cairo_context.set_source_rgb(0, 0, 0)
        # Adicionando o contexto na página.
        PangoCairo.show_layout(cr=cairo_context, layout=self.pango_layout)

    def open_print_dialog(self, widget):
        """Dialogo de impressão do sistema."""
        # Operação de impressão.
        print_operation = self._print_operation()

        # Resposta da operação de impressão.
        response = print_operation.run(
            action=Gtk.PrintOperationAction.PRINT_DIALOG,
            parent=self,
        )
        if response == Gtk.PrintOperationResult.ERROR:
            print('ERROR')
        elif response == Gtk.PrintOperationResult.APPLY:
            print('APPLY')
        elif response == Gtk.PrintOperationResult.CANCEL:
            print('CANCEL')
        elif response == Gtk.PrintOperationResult.IN_PROGRESS:
            print('IN_PROGRESS')

    def open_preview(self, widget):
        """Pré visualizador do sistema."""
        print_operation = self._print_operation()
        print_operation.run(action=Gtk.PrintOperationAction.PREVIEW, parent=self)

    def open_page_setup_dialog(self, widget):
        """Diálogo para configuração da página."""
        # TODO: Fazer funcionar esta operação
        # Verificando o tamanho da página ANTES do diálogo.
        print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))

        self.page_setup = Gtk.print_run_page_setup_dialog(
            parent=self,
            page_setup=self.page_setup,
            settings=self.print_settings,
        )

        # Verificando o tamanho da página DEPOIS do diálogo.
        print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))

    def export_to_pdf(self, widget):
        """Exportando para arquivo."""

        dialog = DialogExportToPdf(self.name)
        dialog.set_transient_for(parent=self)
        response = dialog.run()
        # Verificando a resposta recebida.
        if response == Gtk.ResponseType.OK:
            capivaraFilePdf = dialog.save_file()
            print_operation = self._print_operation()
            print_operation.set_export_filename(capivaraFilePdf)
            response = print_operation.run(
                action=Gtk.PrintOperationAction.EXPORT,
                parent=self,
            )
            if response == Gtk.PrintOperationResult.APPLY:
                print('Arquivo exportado com sucesso')

        dialog.destroy()

    def add_image(self, image):
        #self.context.save()
        self.context.move_to(self.left_margin, self.position_y)
        image_surface = cairo.ImageSurface.create_from_png (image.image_data)
        w = image_surface.get_width()
        h = image_surface.get_height()
        if (self.position_y + h*0.5) > self.ybottom:
            self.page_break()
        data =image_surface.get_data()
        stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_ARGB32, w)
        image_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, w, h,stride)
        self.assert_page_break()
        self.context.scale(0.5, 0.5)
        self.context.set_source_surface(image_surface,self.left_margin/0.5, self.position_y/0.5)
        self.context.paint()
        self.context.restore()
        self.position_y+= h*0.5+ image.padding_bottom