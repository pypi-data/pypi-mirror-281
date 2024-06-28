import { JupyterFrontEnd } from '@jupyterlab/application';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { IRenderMimeRegistry, MimeModel } from '@jupyterlab/rendermime';
import { KernelMessage } from '@jupyterlab/services';
import { v4 as uuid } from 'uuid';

export const exportPDF = async (
  app: JupyterFrontEnd,
  rendermime: IRenderMimeRegistry
) => {
  const nb = app.shell.currentWidget;
  if (!(nb instanceof NotebookPanel) || !nb.model) {
    return;
  }
  const workingKernel = nb.sessionContext.session?.kernel;
  if (!workingKernel) {
    return;
  }

  const [codes, vars] = nb.model.sharedModel.cells
    .filter(({ cell_type }) => cell_type === 'code')
    .map(({ source }) => source)
    .filter(source => !source.startsWith('%?') && !source.startsWith('%%'))
    .map(source => {
      if (source.startsWith('%!')) {
        return [source, null] as [string, null];
      }

      const v = `notebook-export-${uuid()}`;
      const def = `%! val ${v} = '< ${source} >`;
      return [def, v];
    })
    .reduce<[string[], (string | null)[]]>(
      ([a1, a2], [c1, c2]) => [
        [...a1, c1],
        [...a2, c2]
      ],
      [[], []]
    );

  const document = vars
    .filter(v => v)
    .map(v => `#${v};`)
    .join(' ');

  const startKernel = app.serviceManager.kernels.startNew(
    {
      name: workingKernel.name
    },
    {
      clientId: workingKernel.clientId,
      username: workingKernel.username,
      handleComms: workingKernel.handleComms
    }
  );
  const renderingKernel = await ['%% render-in-pdf', ...codes].reduce(
    async (acc, code) =>
      acc.then(
        renderingKernel =>
          new Promise((resolve, reject) => {
            const future = renderingKernel.requestExecute({ code });
            future.onIOPub = msg => {
              if (
                KernelMessage.isStatusMsg(msg) &&
                msg.content.execution_state === 'idle'
              ) {
                resolve(renderingKernel);
              }

              if (KernelMessage.isErrorMsg(msg)) {
                reject(new Error(msg.content.evalue));
              }
            };
          })
      ),
    startKernel
  );
  const future = renderingKernel.requestExecute({ code: document });
  future.onIOPub = msg => {
    if (!KernelMessage.isExecuteResultMsg(msg)) {
      return;
    }

    renderingKernel.shutdown();
    const pdf = rendermime.createRenderer('application/pdf');
    const tab = new MainAreaWidget({
      content: pdf
    });
    tab.title.label = `PDF Export: ${nb.title.label}`;
    tab.id = `${nb.id}-exported-pdf`;
    tab.revealed.then(() => {
      pdf.renderModel(new MimeModel(msg.content));
    });
    app.shell.add(tab, 'main', { mode: 'tab-after' });
  };
};
