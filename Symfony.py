import sublime, sublime_plugin, re, os

wait_file = False
show_action = ''
class SymfonyViewCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global wait_file
		global show_action
		
		if os.sep == '/':
			pathsep = '/'
			regex_pathsep = '/'
		elif os.sep == '\\':
			pathsep = '\\'
			regex_pathsep = '\\\\'


		file = self.view.file_name()
		file_re = re.search('(.+)' + regex_pathsep + '(.+)Controller.php', file)


		if file_re:
			folder = file_re.group(1)
			file = file_re.group(2)
			action = self.view.find("\w+Action", self.view.sel()[0].begin())
			if action:
				line = self.view.word(action)
				line_contents = self.view.substr(line)
				a = re.search('(\w+)Action', line_contents).group(1)
				self.view.window().open_file(folder + pathsep + '..' + pathsep + 'Resources' + pathsep + 'views' + pathsep + file + pathsep + a + '.html.twig')
		elif re.search('(.+)' + regex_pathsep + '(.+).html.twig', file):
			file_re = re.search('(.+)' + regex_pathsep + '(.+)' + regex_pathsep + '(.+).html.twig', file)
			folder = file_re.group(1)
			controller = file_re.group(2)
			action = file_re.group(3)
			view = self.view.window().open_file(folder + pathsep + '..' + pathsep + '..' + pathsep + 'Controller' + pathsep + controller+'Controller.php')
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
