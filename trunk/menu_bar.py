import pygtk
pygtk.require('2.0')
import gtk

class MenuBar(gtk.MenuBar):
	""""""
	def __init__(self, list):
		"""list = [(menu_name=str, [(item_image=stock_item, callback), None=separator])]"""
		gtk.MenuBar.__init__(self)
		for menu in list:
			item = gtk.MenuItem(menu[0])
			self.append(item)
			submenu = gtk.Menu()
			for sub in menu[1]:
				if sub == None:
					subitem = gtk.SeparatorMenuItem()
				elif isinstance(sub[0], gtk.CheckMenuItem):
					subitem = sub[0]
					subitem.set_active(sub[2])
					subitem.connect("toggled", sub[1])
				else:
					subitem = gtk.ImageMenuItem(sub[0])
					subitem.connect("activate", sub[1])
				submenu.append(subitem)
				subitem.show()
			item.set_submenu(submenu)
			item.show()
		self.show()
