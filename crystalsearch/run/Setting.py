class Setting:
    """任务参数类"""

    def __init__(self, setting_dict):
        self.target = setting_dict['target']
        self.query = setting_dict['query']
        self.keep_ring = (setting_dict['keep_ring'] == 'True')
        self.loss = setting_dict['loss']
        self.output_path = setting_dict['output_path']
        self.output_fig = setting_dict['output_fig']
        self.output_res = (setting_dict['output_res'] == 'True')
        self.silent = (setting_dict['silent'] == 'True')

    def to_string(self):
        return 'target=%s query=%s\n keep_ring=%s loss_atom=%s\n' \
               % (self.target, self.query, self.keep_ring, self.loss)
