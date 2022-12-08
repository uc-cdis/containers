// do not open notebooks in a new tab in a faster way, see: https://github.com/jupyter/notebook/issues/4115#issuecomment-616069389
$('a').attr('target', '_self');

require(["base/js/namespace"], function (Jupyter) {
  Jupyter._target = '_self';
});
