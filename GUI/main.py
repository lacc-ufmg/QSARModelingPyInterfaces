import gi

gi.require_version('Gtk', '3.0')
import os
from gi.repository import Gtk
from runCalculations import RunCalculations
import pandas
import random

builder: Gtk.Builder = Gtk.Builder()
builder.add_from_file('qsarmodeling.glade')


class Handler(object):
    ga_config = {}
    ops_config = {}

    def __init__(self):
        # Saving windows
        self.main_window = builder.get_object('main_window')
        self.config_OPS_window = builder.get_object('config_OPS_window')
        self.config_GA_window = builder.get_object('config_GA_window')
        self.about_window = builder.get_object('about_window')
        self.csv_file_filter = builder.get_object('open_filter')
        self.main_window_stack = builder.get_object('main_window_stack')
        self.config_varcut_window = builder.get_object('config_varcut_window')

        # Saving elements
        self.main_window_pages = [builder.get_object('main_window_welcome'), builder.get_object('main_window_tables')]
        self.treeview_X = builder.get_object('treeview_X')
        self.treeview_y = builder.get_object('treeview_y')

        # connect destroy signal
        self.main_window.connect('destroy', Gtk.main_quit)
        self.config_OPS_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.config_GA_window.connect('delete-event', lambda w, e: w.hide() or True)
        self.about_window.connect('delete-event', lambda w, e: w.hide() or True)

        # Setting file filters
        self.csv_file_filter.set_name('CSV Files (*.csv)')

        # Handling files
        self.X_matrix = ""
        self.y_vector = ""
        self.last_opened_path = ""
        self.last_saved_path = ""

    def on_menu_ops_model_activate(self, _):
        self.config_OPS_window.show_all()

    def on_menu_ga_model_activate(self, _):
        self.config_GA_window.show_all()

    def on_menu_varcut_activate(self, _):
        self.config_varcut_window.show()

    def on_OPS_cancel_button_clicked(self, _):
        self.config_OPS_window.hide()

    def on_GA_cancel_button_clicked(self, _):
        self.config_GA_window.hide()

    def on_OPS_run_button_clicked(self, _):
        if self.files_ok():
            self.ops_config = {
                'XMatrix': self.X_matrix,
                'yvector': self.y_vector,
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
                'ops_type': 'f' if builder.get_object('ops_feed_ops').get_active() else 's'
            }

            rand = random.randint(10000, 99999)
            if not self.ops_config['output_matrix']:
                self.ops_config['output_matrix'] = os.path.join(os.path.dirname(self.X_matrix),
                                                                "OPS_output_matrix_{}.csv".format(rand))
            if not self.ops_config['output_cv']:
                self.ops_config['output_cv'] = os.path.join(os.path.dirname(self.X_matrix),
                                                            "OPS_output_CV_{}.csv".format(rand))
            if not self.ops_config['output_models']:
                self.ops_config['output_models'] = os.path.join(os.path.dirname(self.X_matrix),
                                                                "OPS_output_models_{}.csv".format(rand))

            RunCalculations.runOPS(self.ops_config)

            # If everything is ok, current matrix will be the filtered one.
            if os.path.isfile(self.ops_config['output_matrix']):
                self.X_matrix = self.ops_config['output_matrix']
                self.draw_matrices('matrix')
        else:
            print("Please, go to File > Open... before run a calculation.")

    def on_GA_run_button_clicked(self, _):
        if self.files_ok():
            self.ga_config = {
                'XMatrix': self.X_matrix,
                'yvector': self.y_vector,
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

            rand = random.randint(10000, 99999)
            if not self.ga_config['output_matrix']:
                self.ga_config['output_matrix'] = os.path.join(os.path.dirname(self.X_matrix),
                                                               "GA_output_matrix_{}.csv".format(rand))
            if not self.ga_config['output_cv']:
                self.ga_config['output_cv'] = os.path.join(os.path.dirname(self.X_matrix),
                                                           "GA_output_CV_{}.csv".format(rand))
            if not self.ga_config['output_q2']:
                self.ga_config['output_q2'] = os.path.join(os.path.dirname(self.X_matrix),
                                                           "GA_output_Q2_{}.csv".format(rand))
            if not self.ga_config['output_selected']:
                self.ga_config['output_selected'] = os.path.join(os.path.dirname(self.X_matrix),
                                                                 "GA_output_selected_{}.csv".format(rand))

            RunCalculations.runGA(self.ga_config)

            # If everything is ok, current matrix will be the filtered one.
            if os.path.isfile(self.ga_config['output_matrix']):
                self.X_matrix = self.ga_config['output_matrix']
                self.draw_matrices('matrix')
        else:
            print("Please, open the files in File > Open...")

    def on_menu_about_activate(self, _):
        self.about_window.run()

    def open_file(self, use_last_path=True):
        file_chooser = Gtk.FileChooserDialog(title="Open...", action=Gtk.FileChooserAction.OPEN)
        file_chooser.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        file_chooser.set_default_response(Gtk.ResponseType.OK)
        file_chooser.add_filter(self.csv_file_filter)
        if self.last_opened_path and use_last_path:
            file_chooser.set_current_folder(self.last_opened_path)
        response = file_chooser.run()
        filename = None
        if response == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            self.last_opened_path = os.path.dirname(os.path.abspath(filename))
            # entry.set_text(filename)
        file_chooser.destroy()
        return filename

    def on_save_file(self, entry):
        file_chooser = Gtk.FileChooserDialog(title="Save...", action=Gtk.FileChooserAction.SAVE)
        file_chooser.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        file_chooser.set_default_response(Gtk.ResponseType.OK)
        file_chooser.add_filter(self.csv_file_filter)
        if self.last_saved_path:
            file_chooser.set_current_folder(self.last_saved_path)
        elif self.last_opened_path:
            file_chooser.set_current_folder(self.last_opened_path)
        response = file_chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            self.last_saved_path = filename
            entry.set_text(filename)
        file_chooser.destroy()

    def block_menus_until_file_load(self):
        menus = [
            builder.get_object('menu_generate'),
            builder.get_object('menu_validate'),
            builder.get_object('menu_filter'),
            builder.get_object('menu_predict'),
        ]
        if self.X_matrix and self.y_vector:
            for elem in menus:
                elem.set_sensitive(True)
        else:
            for elem in menus:
                elem.set_sensitive(False)

    def on_menu_open_matrix_activate(self, _):
        filename = self.open_file()
        if filename:
            self.X_matrix = filename
            self.draw_matrices('matrix')

    def on_menu_open_vector_activate(self, _):
        filename = self.open_file()
        if filename:
            self.y_vector = filename
            self.draw_matrices('vector')

    def draw_matrices(self, what_to_draw):
        show = False
        if what_to_draw == 'matrix' and self.X_matrix and os.path.isfile(self.X_matrix):
            # Draw matrix
            self.draw_pandas_matrix(self.treeview_X, self.X_matrix)
            show = True
        if what_to_draw == 'vector' and self.y_vector and os.path.isfile(self.y_vector):
            # Draw vector
            self.draw_pandas_vector(self.treeview_y, self.y_vector)
            show = True

        if show:
            self.main_window_stack.set_visible_child(self.main_window_pages[1])
        else:
            self.main_window_stack.set_visible_child(self.main_window_pages[0])

        self.block_menus_until_file_load()

    def draw_pandas_matrix(self, treeview, path, print_index=True):
        df = pandas.read_csv(path, index_col=0)
        print_etc = False
        if df.shape[1] > 10:
            df = df.iloc[:, 0:10]
            print_etc = True
        liststore_args = [str] if print_index else []
        liststore_args += [float] * int(df.shape[1])
        if print_etc:
            liststore_args += [str]
        liststore = Gtk.ListStore(*liststore_args)
        df_indexes = df.index.values
        for i in range(df.shape[0]):
            appendix = [str(df_indexes[i])] if print_index else []
            appendix += list(df.iloc[i, :])
            if print_etc:
                appendix += ["..."]

            liststore.append(appendix)
        self.clear_treeview(treeview)
        current_model = treeview.get_model()
        if current_model is not None:
            current_model.clear()
        treeview.set_model(liststore)

        # Draw index column
        if print_index:
            renderer_text = Gtk.CellRendererText()
            column_text = Gtk.TreeViewColumn('Molecule', renderer_text, text=0)
            treeview.append_column(column_text)

        # Draw data columns
        for i in range(df.shape[1]):
            renderer_text = Gtk.CellRendererText()
            text = i + 1 if print_index else i
            column_text = Gtk.TreeViewColumn(df.columns[i], renderer_text, text=text)
            treeview.append_column(column_text)

        # Draw et cetera column
        if print_etc:
            renderer_text = Gtk.CellRendererText()
            text = df.shape[1] + 1 if print_index else df.shape[1]
            column_text = Gtk.TreeViewColumn('...', renderer_text, text=df.shape[1] + 1)
            treeview.append_column(column_text)

    def draw_pandas_vector(self, treeview, path):
        df = pandas.read_csv(path)

        self.clear_treeview(treeview)

        liststore = Gtk.ListStore(float)

        # df should be a vector
        data = list(df.iloc[0, :]) if df.shape[0] == 1 else list(df.iloc[:, 0])

        for i in range(max(df.shape[0], df.shape[1])):
            liststore.append([data[i]])

        treeview.set_model(liststore)

        # Draw data column
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn('Vector', renderer_text, text=0)
        treeview.append_column(column_text)

    def on_varcut_run_button_clicked(self, _):
        if self.files_ok():
            value = float(builder.get_object('varcut_varcut').get_value())

            """In the future, the user will be able to cut the matrix without 
            saving it, leaving it temporarily available within the program to
            perform another calculation in the sequence."""
            save = True  # builder.get_object('varcut_save').get_active()
            output = builder.get_object('varcut_output').get_text() if save else ""
            new_matrix = RunCalculations.runVarCut(self.X_matrix, value, save, output)
            if os.path.isfile(new_matrix):
                self.X_matrix = new_matrix
                self.draw_matrices('matrix')
            self.config_varcut_window.hide()

    @staticmethod
    def on_auto_state_set(obj, active: bool):
        """Set an object as active (editable) or not. Usually called by switchers."""
        if active:
            obj.set_value(0)
            obj.set_editable(False)
            obj.set_sensitive(False)
        else:
            obj.set_editable(True)
            obj.set_sensitive(True)

    def on_varcut_save_toggled(self, this):
        box = builder.get_object('varcut_filename_box')
        if this.get_active():
            box.show()
        else:
            box.hide()

    def files_ok(self):
        return os.path.isfile(self.X_matrix) and os.path.isfile(self.y_vector)

    @staticmethod
    def on_close_modal(modal):
        modal.hide()

    @staticmethod
    def clear_treeview(treeview):
        columns = treeview.get_columns()
        for col in columns:
            treeview.remove_column(col)

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
