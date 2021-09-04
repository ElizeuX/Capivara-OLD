import gi

gi.require_version(namespace='Gtk', version='3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from gi.repository.GdkPixbuf import Pixbuf

from CharacterCtrl import CharacterControl


class Treeview():
    treeview = None
    treemodel = None
    vo = None

    selected = 'workspace'

    def __init__(self, treeview, data, voCharacter):

        for column in treeview.get_columns():
            treeview.remove_column(column)

        self.treeview = treeview
        self.data = data
        self.vo = voCharacter

        self.treeview.connect('row-activated', self.selection)
        self.treeview.connect('button_press_event', self.mouse_click)

        # create a storage model in this case a treemodel
        self.treemodel = Gtk.TreeStore(str, Pixbuf, str)
        self.treeview.set_model(self.treemodel)
        #self.treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [], DRAG_ACTION)
        # self.drop_area = DropArea()

        # add columns usually only one in case of the treeview
        column = Gtk.TreeViewColumn("Projeto")

        # add in a text renderer so we can see the items we add

        # Create a column cell to display text
        cell = Gtk.CellRendererText()

        # Create a column cell to display an image
        colCellImg = Gtk.CellRendererPixbuf()

        # Add the cells to the column
        column.pack_start(colCellImg, False)
        column.pack_start(cell, True)

        # Bind the text cell to column 0 of the tree's model
        column.add_attribute(cell, "text", 0)

        # Bind the image cell to column 1 of the tree's model
        column.add_attribute(colCellImg, "pixbuf", 1)

        self.treeview.append_column(column)

        # Quando um item é selecionado
        tree_selection = treeview.get_selection()

        # verifico se o handler já está conectado
        handler_id = self.get_handler_id(tree_selection, "changed")

        if handler_id == 0:
            tree_selection.connect("changed", self.onSelectionChanged)

        self.populate()
        treeview.expand_all()
        # selecionar primeiro personagem
        # last = self.treemodel.iter_n_children()
        # last = last - 1  # iter_n_children starts at 1 ; set_cursor starts at 0
        # c = self.treeview.get_column(0)
        # self.treeview.set_cursor(last, c, True)  # set the cursor to the last appended item
        # self.treeview.row_activated(Gtk.TreePath(row), Gtk.TreeViewColumn(None))
        # self.treeview.set_cursor(Gtk.TreePath(row))
        #
        c = self.treeview.get_column(0)
        self.treeview.set_cursor(Gtk.TreePath.new_from_string("0:0"), c,
                                 True)  # set the cursor to the last appended item

        # self.menu()

    def get_handler_id(self, obj, signal_name):
        signal_id, detail = GObject.signal_parse_name(signal_name, obj, True)
        return GObject.signal_handler_find(obj, GObject.SignalMatchType.ID, signal_id, detail, None, None, None)

    def populate(self):
        self.treemodel.clear()

        galhos = self.data.keys()

        for cabec in galhos:
            iter_level_1 = self.append_tree(cabec.capitalize())
            for dados in self.data[cabec]:
                dictlist = []
                for k, v in dados.items():
                    temp = v
                    dictlist.append(temp)
                iter_level_2 = self.append_tree(dictlist[1], dictlist[0], iter_level_1)

    def append_tree(self, name=None, id=None, parent=None):
        """
            append to the treeview if parent is null append to root level.
            if parent is a valid iter (possibly returned from previous append) then append under the parent
        """
        itemIsHeader = parent == None
        itemIcon = Gtk.IconTheme.get_default().load_icon(
            "document-open-symbolic" if itemIsHeader else "user-info-symbolic", 22, 0)
        myiter = self.treemodel.insert_after(parent, None)
        self.treemodel.set_value(myiter, 0, name)
        self.treemodel.set_value(myiter, 1, itemIcon)
        self.treemodel.set_value(myiter, 2, str(id))
        self.order = Gtk.SortType.ASCENDING

        return myiter

    def menu(self):
        """
        popover menu shown on right clicking a treeview item.
        """
        self.treeview_menu = Gtk.Menu()
        menu_item = Gtk.MenuItem("Excluir Capivara")
        self.treeview_menu.append(menu_item)
        menu_item = Gtk.MenuItem("Imprimir Capivara")
        self.treeview_menu.append(menu_item)

        # for item in range(0, 5):
        #     menu_item = Gtk.MenuItem("Menu " + str(item))
        #     self.treeview_menu.append(menu_item)

    def mouse_click(self, tv, event):
        if event.button == 3:
            # right mouse button pressed popup the menu
            self.treeview_menu.show_all()
            self.treeview_menu.popup(None, None, None, None, 1, 0)

    def selection(self, tv, treepath, tvcolumn):
        """
            on double click get the value of the item we clicked
        """
        model = tv.get_model()
        treeiter = model.get_iter(treepath)
        self.selected = model.get_value(treeiter, 1)
        # self.entry.set_text(self.selected)
        print(self.selected)

    def onSelectionChanged(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        if value:
            print(str(value))
            c = CharacterControl(value, self.vo)


