# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from gi.repository.GdkPixbuf import Pixbuf

from DataAccess import Character, Core, SmartGroup, CoreCharacterLink
from CharacterCtrl import CharacterControl
from NewGroupDialog import NewGroupDialog



#### Drag and drop stuff
DRAG_ACTION = Gdk.DragAction.COPY
dnd_internal_target = 'gtg/task-iter-str'
dnd_external_targets ={}

targets = [
    ('text/plain', 0, 0) # have tried various combinations of these
]



class Treeview():
    treeview = None
    treemodel = None
    #vo = None
    dnd_internal_target = 'gtg/task-iter-str'
    # CONSTANTES DO MENU
    __DELETE_CHARACTER = 1
    __DELETE_CORE = 2
    __DELETE_SMARTGROUP = 3
    __PRINT_CAPIVARA = 4
    __DELETE_CAPIVARA = 5
    __REMOVE_CHARACTER_CORE = 6
    __EDIT_SMARTGROUP = 7
    __EDIT_GROUP = 8

    selected = 'workspace'
    widget = ""

    def __init__(self, treeview, widget, vo = None ):

        self.data = vo
        self.widget = widget


        for column in treeview.get_columns():
            treeview.remove_column(column)

        self.treeview = treeview

        self.treeview.connect('row-activated', self.selection)

        self.treeview.connect('button_press_event', self.mouse_click)

        # create a storage model in this case a treemodel
        self.treemodel = Gtk.TreeStore(str, Pixbuf, str)
        self.treeview.set_model(self.treemodel)

        #Drag and drop
        self.__init_dnd()

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
        handler_id = self.get_handler_id(self.treeview, "button_press_event")
        if handler_id == 0:
            tree_selection.connect("button_press_event", self.mouse_click())

        handler_id = self.get_handler_id(tree_selection, "changed")
        if handler_id == 0:
            tree_selection.connect("changed", self.onSelectionChanged)

        handler_id = self.get_handler_id(self.treeview, "drag_data_get")
        if handler_id == 0:
            self.treeview.connect('drag_data_get', on_drag_data_get)

        handler_id = self.get_handler_id(self.treeview, "drag_data_received")
        if handler_id == 0:
            self.treeview.connect('drag_data_received', on_drag_data_received)

        handler_id = self.get_handler_id(self.treeview, "drag_failed")
        if handler_id == 0:
            self.treeview.connect('drag_failed', on_drag_fail)

        self.populate()
        treeview.expand_all()

        c = self.treeview.get_column(0)
        self.treeview.set_cursor(Gtk.TreePath.new_from_string("0:0"), c,
                                 True)  # set the cursor to the last appended item

        self.treeview_menu = Gtk.Menu()



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

        # if dnd_internal_target == '':
        #     error = 'Cannot initialize DND without a valid name\n'
        #     error += 'Use set_dnd_name() first'
        #     raise Exception(error)
        #
        # dnd_targets = [(dnd_internal_target, Gtk.TargetFlags.SAME_WIDGET, 0)]
        # for target in dnd_external_targets:
        #     name = dnd_external_targets[target][0]
        #     dnd_targets.append((name, Gtk.TARGET_SAME_APP, target))

        self.treeview.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                          targets, Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

        self.treeview.enable_model_drag_dest(targets, Gdk.DragAction.DEFAULT | Gdk.DragAction.COPY)

    def get_handler_id(self, obj, signal_name):
        signal_id, detail = GObject.signal_parse_name(signal_name, obj, True)
        return GObject.signal_handler_find(obj, GObject.SignalMatchType.ID, signal_id, detail, None, None, None)

    def populate(self):
        self.treemodel.clear()
        # itemIconHeader = pixbuf = GdkPixbuf.Pixbuf.new_from_file('assets/icons/Apps-file-manager-archive-icon.png')
        # itemIconSmartGroup = pixbuf = GdkPixbuf.Pixbuf.new_from_file('assets/icons/system-file-manager-icon (1).png')
        # itemIconCore = pixbuf = GdkPixbuf.Pixbuf.new_from_file('assets/icons/drawerwithpapers_79615.png')
        # itemIconCharacter = pixbuf = GdkPixbuf.Pixbuf.new_from_file('assets/icons/Files-icon.png')

        # Adicionando Smart Groups
        sg = SmartGroup()
        smartGroups = sg.list()
        character = Character()
        iter_level_1 = self.append_tree("SmartGroups")
        for smartGroup in smartGroups:
            iter_level_2 = self.append_tree(smartGroup.description, smartGroup.id, iter_level_1)
            c = smartGroup.listCharacter(smartGroup.rule)
            for i in c:
                iter_level_3 = self.append_tree(character.get(i.id).name, i.id, iter_level_2)


        # Adicionando núcleos
        c = Core()
        d = Character()
        cores = c.list()
        iter_level_1 = self.append_tree("Cores")
        for core in cores:
            iter_level_2 = self.append_tree(core.description, core.id, iter_level_1)
            characters = c.listCharacters(core.id)
            for i in characters:
                iter_level_3 = self.append_tree(d.get(i.character_id).name, i.character_id, iter_level_2)

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

    # def menu(self):
    #     """
    #     popover menu shown on right clicking a treeview item.
    #     """
    #
    #
    #
    #
    #     # for item in range(0, 5):
    #     #     menu_item = Gtk.MenuItem("Menu " + str(item))
    #     #     self.treeview_menu.append(menu_item)

    def item_activated(self, wdg, i):
        if (i == self.__DELETE_CAPIVARA):
            self.deleteCharacter()
            self.treeview_menu.popdown()

        elif( i == self.__PRINT_CAPIVARA):
            print("Imprimindo capivara")
            self.treeview_menu.popdown()

        elif(i == self.__REMOVE_CHARACTER_CORE):
            self.removeCharacterOfCore()
            self.treeview_menu.popdown()

        elif(i == self.__EDIT_GROUP):
            self.groupEdit()
            self.treeview_menu.popdown()

        elif(i == self.__DELETE_CORE):
            self.deleteCore()
            self.treeview_menu.popdown()

        elif (i == self.__DELETE_SMARTGROUP):
            self.deleteSmartGroup()
            self.treeview_menu.popdown()

        else:
            print(i)

    def mouse_click(self, tv, event):
        if event.button == 3:

            treeselection = self.treeview.get_selection()
            model, paths = treeselection.get_selected_rows()
            iters = [model.get_iter(path) for path in paths]
            iter_str = ','.join([model.get_string_from_iter(iter) for iter in iters])

            if iter_str == '0' or iter_str =='1' or iter_str == '2':
                return

            if iter_str[0] == '2' and len(iter_str)>3:
                return

            # remover todos os itens de menu
            for i in self.treeview_menu.get_children():
                self.treeview_menu.remove(i)

            self.treeview_menu = Gtk.Menu()

            # menu para se header for personagem
            if iter_str[0] == "0":
                menu_item = Gtk.MenuItem("Excluir Capivara")
                self.treeview_menu.append(menu_item)
                menu_item.connect("activate", self.item_activated, self.__DELETE_CAPIVARA)

                menu_item = Gtk.MenuItem("Imprimir Capivara")
                self.treeview_menu.append(menu_item)
                menu_item.connect("activate", self.item_activated, self.__PRINT_CAPIVARA)

            # grupo "1:0"
            elif iter_str[0] == '1':
                # item = 1:0:0
                if len(iter_str) >= 5:
                    menu_item = Gtk.MenuItem("Remover do grupo")
                    self.treeview_menu.append(menu_item)
                    menu_item.connect("activate", self.item_activated, self.__REMOVE_CHARACTER_CORE)
                else:
                    menu_item = Gtk.MenuItem("Editar grupo")
                    self.treeview_menu.append(menu_item)
                    menu_item.connect("activate", self.item_activated, self.__EDIT_GROUP)

                    menu_item = Gtk.MenuItem("Excluir grupo")
                    self.treeview_menu.append(menu_item)
                    menu_item.connect("activate", self.item_activated, self.__DELETE_CORE)

            # smartgrupo = "2:0"
            elif iter_str[0] == "2":
                if len(iter_str) <= 3 :
                    menu_item = Gtk.MenuItem("Excluir smartgroup")
                    self.treeview_menu.append(menu_item)
                    menu_item.connect("activate", self.item_activated, self.__DELETE_SMARTGROUP)

                    menu_item = Gtk.MenuItem("Editar smartgroup")
                    self.treeview_menu.append(menu_item)
                    menu_item.connect("activate", self.item_activated, self.__EDIT_SMARTGROUP)
                else:
                    # remover todos os itens de menu
                    for i in self.treeview_menu.get_children():
                        self.treeview_menu.remove(i)

            value = ""
            for path in paths:
                tree_iter = model.get_iter(path)
                value = model.get_value(tree_iter, 2)
            if value:
                iters = [model.get_iter(path) for path in paths]
                iter_str = ','.join([model.get_string_from_iter(iter) for iter in iters])

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
        #print(self.selected)

    def onSelectionChanged(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        iters = [model.get_iter(path) for path in pathlist]
        iter_str = ','.join([model.get_string_from_iter(iter) for iter in iters])
        # TODO: Resolver essa gambiarra
        if value:
            try:
                c = CharacterControl(value, self.data)
            except:
                pass

    def get_Core_Iter(self):
        pass

    def removeCharacterOfCore(self):
        tree_selection = self.treeview.get_selection()
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        if value:
            c = Character()
            c.removeCharacterOfCore(value)
            model.remove(tree_iter)

    def groupEdit(self):
        tree_selection = self.treeview.get_selection()
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        if value:
            dialog = NewGroupDialog(value)
            dialog.set_transient_for(parent= self.widget)
            response = dialog.run()

            # Verificando qual botão foi pressionado.
            if response == Gtk.ResponseType.YES:
                c = Core()
                c.id = value
                c.description = dialog.newGroup()
                c.update(c)
                model.set_value(tree_iter, 0, c.description)

            dialog.destroy()

    def deleteCharacter(self):
        tree_selection = self.treeview.get_selection()
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        if value:
            c = Character()
            c.delete(value)
            model.remove(tree_iter)

            last = self.treemodel.iter_n_children()
            last = last - 1  # iter_n_children starts at 1 ; set_cursor starts at 0
            c = self.treeview.get_column(0)
            self.treeview.set_cursor(last, c, True)


    def deleteCore(self):
            tree_selection = self.treeview.get_selection()
            (model, pathlist) = tree_selection.get_selected_rows()
            value = ""
            for path in pathlist:
                tree_iter = model.get_iter(path)
                value = model.get_value(tree_iter, 2)
            if value:
                print(value)
                c = Core()
                c.delete(value)
                model.remove(tree_iter)


    def deleteSmartGroup(self):
        tree_selection = self.treeview.get_selection()
        (model, pathlist) = tree_selection.get_selected_rows()
        value = ""
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 2)
        if value:
            print(value)
            c = SmartGroup()
            c.delete(value)
            model.remove(tree_iter)




def on_drag_fail(widget, dc, result):
    print("Failed dragging", widget, dc, result)

def on_drag_data_get(treeview, context, selection, info, timestamp):
    """ Extract data from the source of the DnD operation.
    Serialize iterators of selected tasks in format
    <iter>,<iter>,...,<iter> and set it as parameter of DND """
    model = treeview.get_model()
    treeselection = treeview.get_selection()
    model, paths = treeselection.get_selected_rows()
    iters = [model.get_iter(path) for path in paths]
    iter_str = ','.join([model.get_string_from_iter(iter) for iter in iters])
    #selection.set(dnd_internal_target, 0, iter_str)
    for path in paths:
        tree_iter = model.get_iter(path)
        value = model.get_value(tree_iter, 2)
    if value:
        selection.set_text(str(value), -1)

def on_drag_data_received(treeview, context, x, y, selection, info, timestamp):

    characterId = selection.get_text()

    model = treeview.get_model()
    destination_iter = None
    destination_tid = None
    drop_info = treeview.get_dest_row_at_pos(x, y)
    if drop_info:
        path, position = drop_info
        strPath = path.to_string()
        strPath = strPath.split(":")
        path = path.new_from_string(strPath[0] + ':' + strPath[1])
        destination_iter = model.get_iter(path)

        if destination_iter:
            destination_tid = model.get_value(destination_iter, 2)
            # 1:1
            c = CoreCharacterLink()
            c.character_id = characterId
            c.core_id = destination_tid
            c.insertcoreCharacterLink(c)

    Treeview(treeview, Treeview.widget)

        # Get dragged iter as a TaskTreeModel iter
        # If there is no selected task (empty selection.data),
        # explictly skip handling it (set to empty list)
        # if selection.data == '':
        #     iters = []
        # else:
        # iters = characterId.split(',')
        #
        # dragged_iters = []
        # for iter in iters:
        #     print("Info", info)
        #     if info == 0:
        #         try:
        #             dragged_iters.append(model.get_iter_from_string(iter))
        #         except ValueError:
        #             # I hate to silently fail but we have no choice.
        #             # It means that the iter is not good.
        #             # Thanks shitty Gtk API for not allowing us to test the string
        #             print("Shitty iter", iter)
        #             dragged_iter = None
        #
        #     elif info in dnd_external_targets and destination_tid:
        #         f = dnd_external_targets[info][1]
        #
        #         src_model = context.get_source_widget().get_model()
        #         dragged_iters.append(src_model.get_iter_from_string(iter))
        #
        # for dragged_iter in dragged_iters:
        #     if info == 0:
        #         if dragged_iter and model.iter_is_valid(dragged_iter):
        #             dragged_tid = model.get_value(dragged_iter, 0)
        #             try:
        #                 row = []
        #                 for i in range(model.get_n_columns()):
        #                     row.append(model.get_value(dragged_iter, i))
        #                 # tree.move_node(dragged_tid, new_parent_id=destination_tid)
        #                 print("move_after(%s, %s) ~ (%s, %s)" % (
        #                 dragged_iter, destination_iter, dragged_tid, destination_tid))
        #                 # model.move_after(dragged_iter, destination_iter)
        #                 model.insert(destination_iter, -1, row)
        #                 model.remove(dragged_iter)
        #             except Exception:
        #                 print('Problem with dragging: ')
        #
        #     elif info in dnd_external_targets and destination_tid:
        #         source = src_model.get_value(dragged_iter, 0)
        #         # Handle external Drag'n'Drop
        #         f(source, destination_tid)
        #
        #
        #
        #
