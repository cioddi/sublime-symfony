import sublime, sublime_plugin, re

class SymfonyViewCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file = self.view.file_name()
		file_re = re.search('(.+)\\\\(.+)Controller.php', file)
		if not file_re:
			sublime.status_message('Not a Symfony Controller file')
			return
		folder = file_re.group(1)
		file = file_re.group(2)
		action = self.view.find("\w+Action", self.view.sel()[0].begin())
		if action:
			line = self.view.word(action)
			line_contents = self.view.substr(line)
			a = re.search('(\w+)Action', line_contents).group(1)
			self.view.window().open_file(folder+'\\..\\Resources\\views\\'+file+'\\'+a+'.html.twig')