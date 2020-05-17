import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from runCalculations import RunCalculations

builder: Gtk.Builder = Gtk.Builder()
builder.add_from_file('qsarmodeling.ui')


class Handler(object):

    ga_config = {}
    ops_config = {}

    def __init__(self):
        self.main_window = builder.get_object('main_window')
        self.config_OPS_window = builder.get_object('config_OPS_window')
        self.config_GA_window = builder.get_object('config_GA_window')
        self.about_window = builder.get_object('about_window')
        self.csv_file_filter = builder.get_object('open_filter')

        # connect destroy signal to hide
        self.main_window.connect('destroy', Gtk.main_quit)
        self.config_OPS_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.config_GA_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.about_window.connect('delete-event', lambda w, e: w.hide() or True)

        self.csv_file_filter.set_name('CSV Files (*.csv)')

    def on_menu_ops_model_activate(self, _):
        self.config_OPS_window.show_all()

    def on_menu_ga_model_activate(self, _):
        self.config_GA_window.show_all()

    def on_OPS_cancel_button_clicked(self, _):
        self.config_OPS_window.hide()

    def on_GA_cancel_button_clicked(self, _):
        self.config_GA_window.hide()

    def on_OPS_run_button_clicked(self, _):
        self.ops_config = {
            'XMatrix': builder.get_object('OPS_input_Xmatrix').get_text(),
            'yvector': builder.get_object('OPS_input_yvector').get_text(),
            'output_matrix': builder.get_object('OPS_output_matrix').get_text(),
            'output_cv': builder.get_object('OPS_output_cv').get_text(),
            'output_models': builder.get_object('OPS_output_models').get_text(),
            'varcut': builder.get_object('ops_varcut').get_value(),
            'corrcut': builder.get_object('ops_corrcut').get_value(),
            'autoscale': builder.get_object('ops_autoscale').get_active(),
            'lj_transform': builder.get_object('ops_ljtransform').get_active(),
            'autocorrcut': builder.get_object('ops_autocorrcut').get_value(),
            'latent_vars_ops': builder.get_object('ops_latent_vars_OPS').get_value(),
            'latent_vars_model': builder.get_object('ops_latent_vars_model').get_value(),
            'ops_window': builder.get_object('ops_OPS_window').get_value(),
            'ops_increment': builder.get_object('ops_OPS_increment').get_value(),
            'vars_percentage': builder.get_object('ops_vars_percentage').get_value(),
            'models_to_save': builder.get_object('ops_models_to_save').get_value(),
            'yrand': builder.get_object('ops_yrand').get_value(),
            'lno': builder.get_object('ops_lno').get_value(),
            'ops_type':'f'
        }
        RunCalculations.runOPS(self.ops_config)

    def on_GA_run_button_clicked(self, _):
        self.ga_config = {
            'XMatrix': builder.get_object('GA_input_Xmatrix').get_text(),
            'yvector': builder.get_object('GA_input_yvector').get_text(),
            'output_matrix': builder.get_object('GA_output_matrix').get_text(),
            'output_cv': builder.get_object('GA_output_cv').get_text(),
            'output_q2': builder.get_object('GA_output_q2').get_text(),
            'output_selected': builder.get_object('GA_output_selected_variables').get_text(),
            'varcut': builder.get_object('ga_varcut').get_value(),
            'corrcut': builder.get_object('ga_corrcut').get_value(),
            'autoscale': builder.get_object('ga_autoscale').get_active(),
            'lj_transform': builder.get_object('ga_ljtransform').get_active(),
            'autocorrcut': builder.get_object('ga_autocorrcut').get_value(),
            'max_latent_model': builder.get_object('ga_max_latent_model').get_value(),
            'min_vars_model': builder.get_object('ga_min_vars_model').get_value(),
            'max_vars_model': builder.get_object('ga_max_vars_model').get_value(),
            'population_size': builder.get_object('ga_population_size').get_value(),
            'migration_rate': builder.get_object('ga_migration_rate').get_value(),
            'crossover_rate': builder.get_object('ga_crossover_rate').get_value(),
            'mutation_rate': builder.get_object('ga_mutation_rate').get_value(),
            'generations': builder.get_object('ga_generations').get_value(),
            'yrand': builder.get_object('ga_yrand').get_value(),
            'lno': builder.get_object('ga_lno').get_value()
        }
        RunCalculations.runGA(self.ga_config)

    def on_menu_about_activate(self, _):
        self.about_window.run()

    def on_auto_state_set(self, obj, active):
        if active:
            obj.set_value(0)
            obj.set_editable(False)
            obj.set_sensitive(False)
        else:
            obj.set_editable(True)
            obj.set_sensitive(True)

    def on_open_file(self, entry):
        file_chooser = Gtk.FileChooserDialog(title="Open...",
                                             action=Gtk.FileChooserAction.OPEN)
        file_chooser.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        file_chooser.set_default_response(Gtk.ResponseType.OK)
        file_chooser.add_filter(self.csv_file_filter)
        response = file_chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            entry.set_text(filename)
        file_chooser.destroy()

    def on_save_file(self, entry):
        file_chooser = Gtk.FileChooserDialog(title="Save...",
                                             action=Gtk.FileChooserAction.SAVE)
        file_chooser.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        file_chooser.set_default_response(Gtk.ResponseType.OK)
        file_chooser.add_filter(self.csv_file_filter)
        response = file_chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            entry.set_text(filename)
        file_chooser.destroy()


    @staticmethod
    def on_about_window_destroy(_):
        return True

    @staticmethod
    def gtk_main_quit(_):
        Gtk.main_quit()


if __name__ == '__main__':
    builder.connect_signals(Handler())
    window = builder.get_object('main_window')
    window.show_all()
    Gtk.main()