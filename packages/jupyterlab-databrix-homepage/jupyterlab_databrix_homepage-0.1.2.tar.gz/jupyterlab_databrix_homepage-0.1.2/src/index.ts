import {
    ILabShell,
    ILayoutRestorer,
    JupyterFrontEnd,
    JupyterFrontEndPlugin
  } from '@jupyterlab/application';
  
import {
    ICommandPalette,
    MainAreaWidget,
    WidgetTracker
  } from '@jupyterlab/apputils';
  
import { Widget } from '@lumino/widgets';
import { toArray } from '@lumino/algorithm';  

class databrixWidget extends Widget {
  /**
  * Construct a new databrix widget.
  */
  constructor() {
    super();

    this.addClass('my-apodWidget');

    this.node.innerHTML = `

      <div class="container">
          <h1>Databrix Lab</h1>
          <p class="subtitle">Lernen Sie Data Science und Machine Learning in der Praxis!</p>
      </div>

      <div class="button-container">        
          <button data-commandLinker-command="nbgrader:open-assignment-list" class="button">
              <div class="icon"></div>
              <span>Praxisprojekte starten</span>
          </button>
        
          <button class="button secondary">
              <div class="icon"></div>
              <span>Gruppe wechseln</span>
          </button>
      </div>

      <div class="contact">
              <h2>Kontakt</h2>
              <p>Bei Fragen kontaktieren Sie bitte uns an admin@databrix.org!</p>
      </div>

        `;
  }
}

  /**
   * Initialization data for the jupyterlab_apod extension.
   */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'databrix-homepage',
    description: 'A JupyterLab extension for homepage databrix lab.',
    autoStart: true,
    requires: [ICommandPalette,ILabShell],
    optional: [ILayoutRestorer],   
    activate: activate
};



function activate(app: JupyterFrontEnd,
                  palette: ICommandPalette, 
                  labShell: ILabShell,
                  restorer: ILayoutRestorer | null) {
  console.log('JupyterLab extension databrix homepage is activated!');
  // Declare a widget variable
  let widget: MainAreaWidget<databrixWidget>;

  // Add an application command
  const command: string = 'launcher:create';
  app.commands.addCommand(command, {
    label: 'Databrix Lab Homepage',
    execute: () => {
      if (!widget || widget.isDisposed) {
        const content = new databrixWidget();
        widget = new MainAreaWidget({content});
        widget.id = 'home';
        widget.title.label = 'Databrix Lab Home';
        widget.title.closable = true;
      }

      if (!tracker.has(widget)) {
        // Track the state of the widget for later restoration
        tracker.add(widget);
      }

      if (!widget.isAttached) {
        // Attach the widget to the main work area if it's not there
        app.shell.add(widget, 'main');
      }
      
      app.shell.activateById(widget.id);


      labShell.layoutModified.connect(() => {
        // If there is only a launcher open, remove the close icon.
        widget.title.closable = toArray(app.shell.widgets('main')).length > 1;
      }, widget);
    }
  });
  

  palette.addItem({
    command: command,
    category: ('Databrix')
  });

  // Track and restore the widget state
  let tracker = new WidgetTracker<MainAreaWidget<databrixWidget>>({
    namespace: 'databrix'
  });
  if (restorer) {
    restorer.restore(tracker, {
      command,
      name: () => 'databrix'
    });
  }
}

  
export default plugin;
