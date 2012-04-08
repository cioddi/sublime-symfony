import sublime, sublime_plugin, re

wait_file = False
show_action = ''
class SymfonyViewCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global wait_file
		global show_action
		file = self.view.file_name()
		file_re = re.search('(.+)\\\\(.+)Controller.php', file)
		if file_re:
			folder = file_re.group(1)
			file = file_re.group(2)
			action = self.view.find("\w+Action", self.view.sel()[0].begin())
			if action:
				line = self.view.word(action)
				line_contents = self.view.substr(line)
				a = re.search('(\w+)Action', line_contents).group(1)
				self.view.window().open_file(folder+'\\..\\Resources\\views\\'+file+'\\'+a+'.html.twig')
		elif re.search('(.+)\\\\(.+).html.twig', file):
			file_re = re.search('(.+)\\\\(.+)\\\\(.+).html.twig', file)
			folder = file_re.group(1)
			controller = file_re.group(2)
			action = file_re.group(3)
			view = self.view.window().open_file(folder+'\\..\\..\\Controller\\'+controller+'Controller.php')
			wait_file = True
			show_action = action
		else:
			sublime.status_message('Not a Symfony Controller or View file')

class SymfonyEvent(sublime_plugin.EventListener):
	def on_load(self, view):
		global wait_file
		global show_action
		if wait_file:
			sel = view.find(show_action+"Action", 0)
			view.show(sel)
			wait_file = False