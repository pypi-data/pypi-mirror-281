import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

const updateFavicon = () => {
  const icons = document.getElementsByClassName('favicon');
  for (const icon of icons) {
    icon.setAttribute(
      'href',
      'https://static.elice.io/runbox/images/project/jupyterlab/assets/elice-logo.svg'
    );
  }
};

updateFavicon();

/**
 * Initialization data for the jupyterlab-elice-theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-elice-theme:plugin',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab-elice-theme is activated!');
    const style = 'jupyterlab-elice-theme/index.css';

    manager.register({
      name: 'Elice',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
