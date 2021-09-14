# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from gi.repository.GdkPixbuf import Pixbuf

from DataAccess import Character, Core, SmartGroup
from CharacterCtrl import CharacterControl

DRAG_ACTION = Gdk.DragAction.COPY

dnd_internal_target = ''
dnd_external_targets = {}

TARGETS = [
        ('MY_TREE_MODEL_ROW', Gtk.TargetFlags.SAME_WIDGET, 0),
        ('text/plain', 0, 1),
        ('TEXT', 0, 2),
        ('STRING', 0, 3),
        ]


class Treeview():
    treeview = None
    treemodel = None
    #vo = None


    selected = 'workspace'

    def __init__(self, treeview, vo = None):

        self.data = vo

        for column in treeview.get_columns():
            treeview.remove_column(column)

        self.treeview = treeview

        self.treeview.connect('row-activated', self.selection)
        self.treeview.connect('button_press_event', self.mouse_click)

        # create a storage model in this case a treemodel
        self.treemodel = Gtk.TreeStore(str, Pixbuf, str)
        self.treeview.set_model(self.treemodel)

        self.dnd_internal_target = 'gtk/task-iter-str'
        self.__init_dnd()
        self.treeview.connect('drag_data_get', self.on_drag_data_get)
        self.treeview.connect('drag_data_received', self.on_drag_data_received)
        self.treeview.connect('drag_failed', self.on_drag_fail)


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

        c = self.treeview.get_column(0)
        self.treeview.set_cursor(Gtk.TreePath.new_from_string("0:0"), c,
                                 True)  # set the cursor to the last appended item

        # self.menu()

    def __init_dnd(self):
        """ Initialize Drag'n'Drop support

        Firstly build list of DND targets:
            * name
            * scope - just the same widget / same application
            * id

        Enable DND by calling enable_model_drag_dest(),
        enable_model-drag_source()

        It didnt use support from Gtk.Widget(drag_source_set(),
        drag_dest_set()). To know difference, look in PyGTK FAQ:
        http://faq.pygtk.org/index.py?file=faq13.033.htp&req=show
        """
        # defer_select = False

        if self.dnd_internal_target == '':
            error = 'Cannot initialize DND without a valid name\n'
            error += 'Use set_dnd_name() first'
            raise Exception(error)

        dnd_targets = [(dnd_internal_target, Gtk.TargetFlags.SAME_WIDGET, 0)]
        for target in dnd_external_targets:
            name = dnd_external_targets[target][0]
            dnd_targets.append((name, Gtk.TARGET_SAME_APP, target))

        self.treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                    dnd_targets, Gdk.DragAction.DEFAULT | DRAG_ACTION)

        self.treeview.enable_model_drag_dest(dnd_targets, Gdk.DragAction.DEFAULT | DRAG_ACTION)

        self.treeview.drag_dest_add_text_targets()
        self.treeview.drag_source_add_text_targets()

    def on_drag_fail(widget, dc, result):
        print("Failed dragging", widget, dc, result)

    def on_drag_data_get(self, treeview, context, selection, info, timestamp):
        print("on_drag_data_get(", treeview, context, selection, info, timestamp)
        treeselection = treeview.get_selection()
        model, paths = treeselection.get_selected_rows()
        iters = [model.get_iter(path) for path in paths]
        iter_str = ','.join([model.get_string_from_iter(iter) for iter in iters])
        #data = model.get_value(iter, 0)
        #selection.set(selection.get_taget(), 0, iter_str)
        selection.set(selection.get_target(),  0, 1 )
        #self, iter_str)

        print("Sending", iter_str)

    def on_drag_data_received(self, treeview, context, x, y, selection, info, \
                              timestamp):
        print("on_drag_data_received", treeview, context, x, y, selection, info, timestamp)
        text = selection.get_text()
        print(text)


    def get_handler_id(self, obj, signal_name):
        signal_id, detail = GObject.signal_parse_name(signal_name, obj, True)
        return GObject.signal_handler_find(obj, GObject.SignalMatchType.ID, signal_id, detail, None, None, None)

    def populate(self):
        self.treemodel.clear()

        # Adicionando Smart Groups
        c = SmartGroup()
        smartGroups = c.list()
        iter_level_1 = self.append_tree("SmartGroups")
        for smartGroup in smartGroups:
            iter_level_2 = self.append_tree(smartGroup.description, smartGroup.id, iter_level_1)

        # Adicionando núcleos
        c = Core()
        cores = c.list()
        iter_level_1 = self.append_tree("Cores")
        for core in cores:
            iter_level_2 = self.append_tree(core.description, core.id, iter_level_1)

        # Adicionando personagens
        c = Character()
        characters = c.list()
        iter_level_1 = self.append_tree("Character")
        for character in characters:
            iter_level_2 = self.append_tree(character.name, character.id, iter_level_1)

    def append_tree(self, name=None, id=None, parent=None):
        """
            append to the treeview if parent is null append to root level.
            if parent is a valid iter (possibly returned from previous append) then append under the parent
        """
        itemIsHeader = parent == None
        itemIcon = Gtk.IconTheme.get_default().load_icon(
            "system-file-manager-symbolic" if itemIsHeader else "document-open-symbolic", 22, 0)
        myiter = self.treemodel.insert_after(parent, None)
        self.treemodel.set_value(myiter, 0, name)
        self.treemodel.set_value(myiter, 1, itemIcon)
        self.treemodel.set_value(myiter, 2, str(id))
        self.order = Gtk.SortType.ASCENDING
        self.treemodel.set_sort_column_id(2, self.order)

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
        self.selected = model.get_value(treeiter, 0)
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
            c = CharacterControl(value, self.data)

    def get_Core_Iter(self):
        pass

