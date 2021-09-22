import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk


class SmartGroupDialog(Gtk.Dialog):

    SmartGroupRule = []

    def __init__(self, parent):
        super().__init__(title="Capivara SmartGroup", transient_for=parent, flags=0)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.set_border_width(10)
        self.set_title("Capivara SmartGroup")
        self.set_default_size(800, 600)

        scrolledwindow = Gtk.ScrolledWindow()


        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)



        # hbox = Gtk.Box(spacing=10)
        # button = Gtk.Button.new_with_label("Listaar")
        # button.connect("clicked", self.on_list_me_clicked, vbox)
        # hbox.pack_start(button, False, False, 0)
        # vbox.add(hbox)

        hbox = Gtk.Box(spacing=10)
        # hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        label = Gtk.Label(label="SmartGroup Name")
        label.set_width_chars(5)
        vbox_left.pack_start(label, False, False, 0)
        vbox.add(hbox)

        self.entrySmartGroup = Gtk.Entry()
        self.entrySmartGroup.set_text('')
        self.entrySmartGroup.set_width_chars(5)
        vbox_right.pack_start(self.entrySmartGroup, False, False, 0)
        vbox.add(hbox)

        hbox = Gtk.Box(spacing=10)
        # hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        # self.rulemaster_store = Gtk.ListStore(str, str)
        # self.rulemaster_store.append(["any", "any"])
        # self.rulemaster_store.append(["all", "all"])

        masterRules = [
            "any",
            "all",
        ]

        self.rulemaster_combo = Gtk.ComboBoxText()
        self.rulemaster_combo.set_entry_text_column(0)
        # rulemaster_combo.connect("changed", self.on_name_combo_changed())
        for masterRule in masterRules:
            self.rulemaster_combo.append_text(masterRule)

        self.rulemaster_combo.set_active(0)

        # rulemaster_combo = Gtk.ComboBox.new_with_model_and_entry(self.rulemaster_store)
        # rulemaster_combo.connect("changed", self.on_name_combo_changed)
        # rulemaster_combo.set_entry_text_column(1)

        vbox_left.pack_start(self.rulemaster_combo, True, True, 0)

        label = Gtk.Label(label="of the following are true")
        vbox_right.pack_start(label, True, True, 0)

        vbox.add(hbox)

        self.name_store = Gtk.ListStore(str, str)
        self.name_store.append(["name", "name"])
        self.name_store.append(["style", "style"])
        self.name_store.append(["ethnicity", "ethnicity"])
        self.name_store.append(["hobbies", "hobbies"])
        self.name_store.append(["eye_color", "eye color"])
        self.name_store.append(["hair_color", "hair color"])

        self.operator_store = Gtk.ListStore(str, str)
        self.operator_store.append(["CONTAINS[cd]", "contains"])
        self.operator_store.append(["BEGINSWITH[cd]", "begins with"])
        self.operator_store.append(["ENDWITH[cd]", "end with"])
        self.operator_store.append(["==[cd]", "is"])
        self.operator_store.append(["!=[cd]", "is not"])

        # self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # self.add(self.vbox)

        hbox = Gtk.Box(spacing=6)
        vbox.add(hbox)

        name_combo = Gtk.ComboBox.new_with_model_and_entry(self.name_store)
        #name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)
        hbox.pack_start(name_combo, False, False, 0)

        operator_combo = Gtk.ComboBox.new_with_model_and_entry(self.operator_store)
        #operator_combo.connect("changed", self.on_operator_combo_changed)
        operator_combo.set_entry_text_column(1)
        hbox.pack_start(operator_combo, False, False, 0)

        entry = Gtk.Entry()
        entry.set_text('')
        entry.set_width_chars(60)
        hbox.pack_start(entry, False, False, 0)

        button = Gtk.Button.new_with_label("-")
        button.connect("clicked", self.on_click_me_clicked, (scrolledwindow, vbox))
        hbox.pack_start(button, False, False, 0)

        button2 = Gtk.Button.new_with_label("+")
        button2.connect("clicked", self.on_click_me_clicked, (scrolledwindow, vbox))
        hbox.pack_start(button2, False, False, 0)

        vbox.pack_start(hbox, False, False, 0)

        self.box = self.get_content_area()
        self.box.add(vbox)
        scrolledwindow.add(vbox)
        self.box.add(scrolledwindow)
        #self.add(scrolledwindow)
        self.data = vbox

        self.box.show_all()




    def on_click_me_clicked(self, button, data):
        scrolledwindow = data[0]
        vbox = data[1]

        #vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox = Gtk.Box(spacing=6)
        vbox.add(hbox)

        name_combo = Gtk.ComboBox.new_with_model_and_entry(self.name_store)
        #name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)
        hbox.pack_start(name_combo, False, False, 0)

        operator_combo = Gtk.ComboBox.new_with_model_and_entry(self.operator_store)
        #operator_combo.connect("changed", self.on_operator_combo_changed)
        operator_combo.set_entry_text_column(1)
        hbox.pack_start(operator_combo, False, False, 0)

        entry = Gtk.Entry()
        entry.set_text('')
        entry.set_width_chars(60)
        hbox.pack_start(entry, False, False, 0)

        button = Gtk.Button.new_with_label("-")
        button.connect("clicked", self.on_click_me_clicked, (scrolledwindow, vbox) )
        hbox.pack_start(button, False, False, 0)

        button2 = Gtk.Button.new_with_label("+")
        button2.connect("clicked", self.on_click_me_clicked, (scrolledwindow, vbox))
        hbox.pack_start(button2, False, False, 0)


        self.box.show_all()

    def getRule(self):
        masterRule = self.rulemaster_combo.get_active_text()
        smartGroupName = self.entrySmartGroup.get_text()
        vbox = self.data

        self.SmartGroupRule = []
        strRule = ''

        for child in vbox.get_children():

            for child2 in child.get_children():
                # se for combo pega get_active()
                if type(child2) == Gtk.ComboBox:
                    tree_iter = child2.get_active_iter()
                    if tree_iter is not None:
                        model = child2.get_model()
                        valor = model[tree_iter][0]
                        strRule = strRule + ' ' + valor

                elif type(child2) == Gtk.Entry:
                    valor = child2.get_text()
                    if valor:
                        strRule = strRule + ' "' + valor.upper() + '"'

                elif type(child2) == Gtk.ComboBoxText:
                    masterRule = child2.get_active_text()
                else:
                    if strRule:
                        self.SmartGroupRule.append(strRule)
                    strRule = ''
        final_str = ""
        if masterRule == 'any':
            final_str = ' OR '.join(self.SmartGroupRule)
        elif masterRule == 'all':
            final_str = ' AND '.join(self.SmartGroupRule)

        '''Retorna lista com o nome do grupo, a regra master e as regras'''
        return [smartGroupName, '('+ final_str + ')']