require([
  'nbextensions/vim_binding/vim_binding',
], function() {
  // Map jj to <Esc>
  CodeMirror.Vim.map("jj", "<Esc>", "insert");
  CodeMirror.Vim.map("H", "^", "normal");
  CodeMirror.Vim.map("L", "$", "normal");
  CodeMirror.Vim.map("r", "<C-r>", "normal");
});
