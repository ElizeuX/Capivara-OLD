import gi

gi.require_version(namespace='Gtk', version='3.0')
gi.require_version(namespace='PangoCairo', version='1.0')

from gi.repository import Gio, Gtk, Pango, PangoCairo

class PrintOperation(Gtk.PrintOperation):

    def __init__(self, text_buffer):
        super().__init__()

        # Operação de impressão.
        self.set_n_pages(1)
        # self.set_default_page_setup(default_page_setup=page_setup)
        self.connect('begin-print', self.begin_print, text_buffer)
        self.connect('draw_page', self.draw_page)

        self.pango_layout = None

    def begin_print(self, print_operation, context, text_view_buffer):
        """Quando a operação de impressão é iniciada."""
        # Posição inicial e final do texto no Gtk.TextView.
        start, stop = text_view_buffer.get_bounds()
        # Texto que está no Gtk.TextView.
        text = text_view_buffer.get_text(
            start=start,
            end=stop,
            include_hidden_chars=True,
        )
        self.pango_layout = context.create_pango_layout()
        self.pango_layout.set_markup(text=text, length=-1)
        self.pango_layout.set_font_description(
            Pango.FontDescription('Arial 12'),
        )

    def draw_page(self, print_operation, context, page_nr):
        """Desenhando a página."""
        cairo_context = context.get_cairo_context()
        # Cor da fonte.
        cairo_context.set_source_rgb(0, 0, 0)
        # Criando o conteudo na página.
        PangoCairo.show_layout(cr=cairo_context, layout=self.pango_layout)

    def page_setup(self):
        """Configuração padrão para o papel."""
        # Tamanho do papel.
        paper_size = Gtk.PaperSize.new(name=Gtk.PAPER_NAME_A4)

        # Configurações da página.
        page_setup = Gtk.PageSetup.new()
        page_setup.set_paper_size_and_default_margins(size=paper_size)
        return page_setup

    def custom_page_setup(self):
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

