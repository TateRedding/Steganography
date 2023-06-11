import gi, os, re
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from PIL import Image
from os.path import exists

class MainWindow(Gtk.Window):

    encode_unsaved_changes = False
    encode_image_uploaded = False
    encode_func_run = False
    encode_image_path = ""
    text_file_contents = ""

    decode_unsaved_changes = False
    decode_image_uploaded = False
    decode_func_run = False
    decode_image_path = ""
    decoded_message = ""

    max_char = 0
    char_count = 0

    image_to_save = Image.new("RGB", (0,0))

    def __init__(self):
        Gtk.Window.__init__(self, title="Steganography")
        self.set_default_size(500, 500)
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Encode Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

        box_encode = Gtk.Box()
        box_encode.set_border_width(10)
        self.notebook.append_page(box_encode, Gtk.Label(label="Encode Message"))

        grid_encode = Gtk.Grid(column_spacing = 10, row_spacing = 10, column_homogeneous = True)
        box_encode.add(grid_encode)

        # 'New' button on encode tab

        new_button_encode = Gtk.Button(label="New")
        new_button_encode.connect("clicked", self.new_project)
        grid_encode.attach(new_button_encode, 0, 0, 1, 1)

        # 'Exit' button on encode tab

        exit_button_encode = Gtk.Button(label="Exit")
        exit_button_encode.connect("clicked", self.exit_program)
        grid_encode.attach(exit_button_encode, 1, 0, 1, 1)

        # 'Upload Image' button on encode tab

        upload_image_encode = Gtk.Button(label="Upload Image")
        upload_image_encode.connect("clicked", self.upload_image_encode)
        grid_encode.attach(upload_image_encode, 0, 1, 1, 1)

        # 'Upload Text' button

        upload_text = Gtk.Button(label="Upload Text")
        upload_text.connect("clicked", self.upload_text)
        grid_encode.attach(upload_text, 1, 1, 1, 1)

        # A label above image area to display image dimesntions or tell the user to upload an image

        self.encode_image_label = Gtk.Label(label="Upload an image to update maximum character count")
        grid_encode.attach(self.encode_image_label, 0, 2, 1, 1)

        # Max character count

        self.max_char_label = Gtk.Label(label="Maxium characters: unknown")
        grid_encode.attach(self.max_char_label, 1, 2, 1, 1)

        # Save a spot for the display image

        self.encode_display_image = Gtk.Image()

        encode_display_box = Gtk.Box()
        encode_display_box.set_size_request(300, 300)
        encode_display_box.set_homogeneous(True)
        encode_display_box.add(self.encode_display_image)

        image_frame_encode = Gtk.Frame()
        image_frame_encode.add(encode_display_box)

        grid_encode.attach(image_frame_encode, 0, 3, 1, 1)

        # Editable, scrollable, and framed text area

        self.text_box_encode = Gtk.TextView()
        self.text_box_encode.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.text_box_encode.set_top_margin(10)
        self.text_box_encode.set_bottom_margin(10)
        self.text_box_encode.set_left_margin(10)
        self.text_box_encode.set_right_margin(10)

        self.text_buffer_encode = self.text_box_encode.get_buffer()
        self.text_buffer_encode.set_text("Enter your message here or upload from a file")
        self.text_buffer_encode.connect("changed", self.text_changes_made)
        self.char_count = self.text_buffer_encode.get_char_count()

        text_frame_encode = Gtk.Frame()
        text_frame_encode.add(self.text_box_encode)

        text_scroll_encode = Gtk.ScrolledWindow()
        text_scroll_encode.set_min_content_width(300)
        text_scroll_encode.set_min_content_height(300)
        text_scroll_encode.add(text_frame_encode)
        grid_encode.attach(text_scroll_encode, 1, 3, 1, 1)

        # 'Encode' button

        encode_button = Gtk.Button(label="Encode")
        encode_button.connect("clicked", self.encode)
        grid_encode.attach(encode_button, 0, 4, 1, 1)

        # Character count

        self.char_count_label = Gtk.Label(label="Character count: " + str(self.char_count))
        grid_encode.attach(self.char_count_label, 1, 4, 1, 1)

        # Encode warning label if no image is uploaded or message is too long

        self.upload_warning_encode = Gtk.Label()
        grid_encode.attach(self.upload_warning_encode, 0, 5, 1, 1)

        # Too many characters warning

        self.too_many_char = Gtk.Label()
        grid_encode.attach(self.too_many_char, 1, 5, 1, 1)

        # Save a spot for the encoded image

        self.final_display_image = Gtk.Image()

        final_display_box = Gtk.Box()
        final_display_box.set_size_request(300, 300)
        final_display_box.set_homogeneous(True)
        final_display_box.add(self.final_display_image)

        image_frame_final = Gtk.Frame()
        image_frame_final.add(final_display_box)

        grid_encode.attach(image_frame_final, 0, 6, 2, 1)

        # 'Save' button for encode tab

        save_encode = Gtk.Button(label="Save Image")
        save_encode.connect("clicked", self.save_image)
        grid_encode.attach(save_encode, 0, 7, 2, 1)

        # Warning if user tries to save without encoding

        self.encode_save_warning = Gtk.Label(label="")
        grid_encode.attach(self.encode_save_warning, 0, 8, 2, 1)

        ### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Decode Tab ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

        box_decode = Gtk.Box()
        box_decode.set_border_width(10)
        self.notebook.append_page(box_decode, Gtk.Label(label="Decode Message"))

        grid_decode = Gtk.Grid(column_spacing = 10, row_spacing = 10, column_homogeneous = True)
        box_decode.add(grid_decode)

        # 'New' button on decode tab

        new_button_decode = Gtk.Button(label="New")
        new_button_decode.connect("clicked", self.new_project)
        grid_decode.attach(new_button_decode, 0, 0, 1, 1)

        # 'Exit' button on decode tab

        exit_button_decode = Gtk.Button(label="Exit")
        exit_button_decode.connect("clicked", self.exit_program)
        grid_decode.attach(exit_button_decode, 1, 0, 1, 1)

        # 'Upload Image' button on decode tab

        upload_image_decode = Gtk.Button(label="Upload Image")
        upload_image_decode.connect("clicked", self.upload_image_decode)
        grid_decode.attach(upload_image_decode, 0, 1, 2, 1)

        # A label above image area to display image dimesntions or tell the user to upload an image

        self.decode_image_label = Gtk.Label(label="Actual image size: ?x?")
        grid_decode.attach(self.decode_image_label, 0, 2, 2, 1)

        # Save a spot for the image to decode

        self.decode_display_image = Gtk.Image()

        decode_display_box = Gtk.Box()
        decode_display_box.set_size_request(612, 300)
        decode_display_box.set_homogeneous(True)
        decode_display_box.add(self.decode_display_image)

        image_frame_decode = Gtk.Frame()
        image_frame_decode.add(decode_display_box)

        grid_decode.attach(image_frame_decode, 0, 3, 2, 1)

        # 'Decode' button

        decode_button = Gtk.Button(label="Decode")
        decode_button.connect("clicked", self.decode)
        grid_decode.attach(decode_button, 0, 4, 2, 1)

        # Please upload image warning for decode tab

        self.upload_warning_decode = Gtk.Label()
        grid_decode.attach(self.upload_warning_decode, 0, 5, 2, 1)

        # Uneditable text area to show decoded Message

        self.text_box_decode = Gtk.TextView()
        self.text_box_decode.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.text_box_decode.set_top_margin(10)
        self.text_box_decode.set_bottom_margin(10)
        self.text_box_decode.set_left_margin(10)
        self.text_box_decode.set_right_margin(10)
        self.text_box_decode.set_editable(False)
        self.text_box_decode.set_cursor_visible(False)

        self.text_buffer_decode = self.text_box_decode.get_buffer()

        text_frame_decode = Gtk.Frame()
        text_frame_decode.add(self.text_box_decode)

        scrolled_window_decode = Gtk.ScrolledWindow()
        scrolled_window_decode.set_min_content_width(300)
        scrolled_window_decode.set_min_content_height(300)
        scrolled_window_decode.add(text_frame_decode)
        grid_decode.attach(scrolled_window_decode, 0, 6, 2, 1)

        # Save button for decode tab

        save_decode = Gtk.Button(label="Save Message")
        save_decode.connect("clicked", self.save_text)
        grid_decode.attach(save_decode, 0, 7, 2, 1)

        # Warning if user tries to save without decoding

        self.decode_save_warning = Gtk.Label(label="")
        grid_decode.attach(self.decode_save_warning, 0, 8, 2, 1)

    def new_project(self, widget): # Reset program to it's original state

        if self.encode_unsaved_changes == True or self.decode_unsaved_changes == True:
            dialog = Unsaved_Dialog(self, "new")
            response = dialog.run()

            if response == Gtk.ResponseType.OK:

                self.reset_window()
            dialog.destroy()

        else:
            self.reset_window()

    def exit_program(self, widget): # Exit program

        if self.encode_unsaved_changes == True or self.decode_unsaved_changes == True:
            dialog = Unsaved_Dialog(self, "exit")
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                Gtk.main_quit()
            dialog.destroy()
        else:
            Gtk.main_quit()

    def resize_image(self, image, max):

        w = image.get_width()
        h = image.get_height()

        if w >= h:
            longest_side = w
        else:
            longest_side = h

        perc = max/longest_side

        return image.scale_simple(perc * w, perc * h, GdkPixbuf.InterpType.BILINEAR)

    def upload_image_encode(self, widget): # Upload an image that will contain the message

        dialog = Gtk.FileChooserDialog(title="Select an image", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name(".png, .jpg, .jpeg")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:

            # Determine maximum character count based on size of the uploaded image and display the image

            self.encode_image_path = dialog.get_filename()

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(dialog.get_filename())

            self.max_char = (pixbuf.get_width() * pixbuf.get_height()) * 3 // 8
            self.max_char_label.set_text("Maxiumum characters: " + str(self.max_char))
            self.encode_image_label.set_text("Actual image size: " + str(pixbuf.get_width()) + " x " + str(pixbuf.get_height()))

            if pixbuf.get_width() > 1500 or pixbuf.get_height() > 1500:
                self.upload_warning_encode.set_text("Large images may take a while to encode")
            else:
                self.upload_warning_encode.set_text("")


            if pixbuf.get_width() > 300 or pixbuf.get_height() > 300:
                pixbuf = self.resize_image(pixbuf, 300)
            self.encode_display_image.set_from_pixbuf(pixbuf)

            self.encode_save_warning.set_text("")
            self.final_display_image.clear()
            self.encode_image_uploaded = True
            self.encode_unsaved_changes = True

            if self.char_count > self.max_char:
                self.too_many_char.set_markup("<span foreground='red'>Too many characters!</span>")
            else:
                self.too_many_char.set_text("")

        dialog.destroy()

    def upload_image_decode(self, widget): # Upload an image that contains a hidden message

        dialog = Gtk.FileChooserDialog(title="Select an image", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name(".png, .jpg, .jpeg")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        dialog.add_filter(filter)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:

            self.decode_image_path = dialog.get_filename()

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.decode_image_path)

            self.decode_image_label.set_text("Actual image size: " + str(pixbuf.get_width()) + " x " + str(pixbuf.get_height()))

            if pixbuf.get_width() > 1500 or pixbuf.get_height() > 1500:
                self.upload_warning_decode.set_text("Large images may take a while to decode")
            else:
                self.upload_warning_decode.set_text("")

            if pixbuf.get_width() > 300 or pixbuf.get_height() > 300:
                pixbuf = self.resize_image(pixbuf, 300)
            self.decode_display_image.set_from_pixbuf(pixbuf)

            self.decode_image_uploaded = True
            self.decode_unsaved_changes = True
            self.text_buffer_decode.set_text("")

        dialog.destroy()

    def upload_text(self, widget): # Choose a text file to be the message

        dialog = Gtk.FileChooserDialog(title="Select a text file", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name(".txt")
        filter.add_pattern("*.txt")

        dialog.add_filter(filter)

        response = dialog.run()

        # Open the chosen file and write it's contents into the text box

        if response == Gtk.ResponseType.OK:
            handle = open(dialog.get_filename())
            text = handle.read()
            if text.isascii() == False:
                ascii_dialog = Non_ASCII(self)
                ascii_dialog.run()
                ascii_dialog.destroy()
            else:
                self.text_file_contents = text
                self.text_buffer_encode.set_text("File uploaded: " + dialog.get_filename())
                self.text_box_encode.set_editable(False)
                self.text_box_encode.set_cursor_visible(False)
                self.encode_unsaved_changes = True

        dialog.destroy()

    def text_changes_made(self, widget): # Update character count and self.encode_unsaved_changes when any changes to the text box are made
        if self.text_file_contents == "":
            self.char_count = self.text_buffer_encode.get_char_count()
        else:
            self.char_count = len(self.text_file_contents)
        self.char_count_label.set_text("Character count: " + str(self.char_count))

        if self.char_count > self.max_char and self.max_char > 0:
            self.too_many_char.set_markup("<span foreground='red'>Too many characters!</span>")
        else:
            self.too_many_char.set_text("")

        self.encode_unsaved_changes = True

    def encode(self, widget): # Encode the message into the image

        if self.encode_image_uploaded == False:
            self.upload_warning_encode.set_text("Please upload an image to encode!")
        elif self.char_count > self.max_char:
            self.upload_warning_encode.set_text("Message is too long to encode!")
        elif self.text_buffer_encode.get_text(self.text_buffer_encode.get_start_iter(), self.text_buffer_encode.get_end_iter(), False ).isascii() == False:
            ascii_dialog = Non_ASCII(self)
            ascii_dialog.run()
            ascii_dialog.destroy()
        else:

            # Convert message to string of 8 bit binary values

            if self.text_file_contents == "":
                binary_values = (' '.join(format(ord(x), 'b') for x in self.text_buffer_encode.get_text(self.text_buffer_encode.get_start_iter(), self.text_buffer_encode.get_end_iter(), False )))
            else:
                binary_values = (' '.join(format(ord(x), 'b') for x in self.text_file_contents))

            eight_bit_values = []
            for value in binary_values.split():
                while len(value) < 8:
                    value = "0" + value
                eight_bit_values.append(value)
            binary_message = "".join(eight_bit_values)

            # For each pixel in the image, convert all RGB values to even numbers.

            base = Image.open(self.encode_image_path).convert("RGB")
            progress = 0
            for x in range(base.width):
                for y in range(base.height):
                    coord = x, y
                    px = list(base.getpixel(coord))
                    npx = [x - 1 if x % 2 == 1 else x for x in px]
                    base.putpixel(coord, tuple(npx))

            # Then, for each RGB value in each pixel, convert the values to represent a 1 or a 0 in the binary message
            # by converting the value to an odd number to represent a 1, or leaving it even to represent a 0.
            # Each pixel will contain 3 bits of the message.

            idx = 0
            end = False
            for x in range(base.width):
                for y in range(base.height):
                    coord = x, y
                    px = list(base.getpixel(coord))
                    for i in range(len(px)):
                        if binary_message[idx] == "1":
                            px[i] += 1
                        idx += 1
                        if idx >= len(binary_message):
                            end = True
                            break
                    base.putpixel(coord, tuple(px))
                    if end == True: break
                if end == True: break

            # Save resulting image to a temp file, display the image, then delete temp file

            temp_file_name = self.encode_image_path.split("/")[-1][:-4] + "_temp.png"
            base.save(temp_file_name)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(temp_file_name)
            if pixbuf.get_width() > 300 or pixbuf.get_height() > 300:
                pixbuf = self.resize_image(pixbuf, 300)
            self.final_display_image.set_from_pixbuf(pixbuf)

            os.remove(temp_file_name)
            self.image_to_save = base

            self.encode_func_run = True
            self.encode_save_warning.set_text("")
            self.encode_unsaved_changes = True

    def decode(self, widget): # Decode the message from the uploaded image

        if self.decode_image_uploaded == False:
            self.upload_warning_decode.set_text("Please upload an image to decode!")
        else:

            # For each RBG value in each image pixel, if the value is even, add a 0 to the binary string,
            # or a 1 if the value if odd

            img = Image.open(self.decode_image_path)
            decoded_binary = ""

            for x in range(img.width):
                for y in range(img.height):
                    coord = x, y
                    px = img.getpixel(coord)
                    for value in px:
                        if value % 2 == 0:
                            decoded_binary += "0"
                        else:
                            decoded_binary += "1"

            # Add spaces every 8 digits to the binary string to split into individual character values

            idx = 0
            decoded_binary_with_spaces = ""
            while idx <= len(decoded_binary):
                binary_char = decoded_binary[idx:idx+8]
                idx += 8
                decoded_binary_with_spaces += binary_char + " "

            # Convert 8 digit binary strings to ASCII characters and strip off all of the "\x00" characters at the end
            # These are added as a result of every pixel value being a 0 after the message is finished in the encoding process

            binary_values = decoded_binary_with_spaces.split()
            ascii_string = ""
            for value in binary_values:
                integer = int(value, 2)
                char = chr(integer)
                ascii_string += char
            self.decoded_message = ascii_string.strip("\x00")

            # Display the results

            if len(self.decoded_message) > 1000:
                self.upload_warning_decode.set_text("Only the first 1000 characters of the message are being displayed. Save the message and open the resulting .txt file\nin order to read the entire message")
                self.text_buffer_decode.set_text(self.decoded_message[:1000])
            else:
                self.text_buffer_decode.set_text(self.decoded_message)

            self.decode_func_run = True
            self.decode_save_warning.set_text("")
            self.decode_unsaved_changes = True

    def save_image(self, widget): # Save the image with an encoded message as a .png file

        if self.encode_func_run == True:
            done = False
            file_dialog = Gtk.FileChooserDialog(title="Save Image", parent=self, action=Gtk.FileChooserAction.SAVE)
            file_dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)

            filter = Gtk.FileFilter()
            filter.set_name(".png")
            filter.add_pattern("*.png")

            file_dialog.add_filter(filter)
            file_dialog.set_current_name(".png")

            while done == False:
                file_response = file_dialog.run()

                if file_response == Gtk.ResponseType.OK:
                    file_name = file_dialog.get_filename()
                    if not file_name.endswith(".png"):
                        file_name += ".png"

                    if exists(file_name):
                        save_dialog = Overwrite_Save(self)
                        save_response = save_dialog.run()

                        if save_response == Gtk.ResponseType.OK:
                            self.image_to_save.save(file_name)
                            self.encode_unsaved_changes = False
                            done = True
                            file_dialog.destroy()
                        save_dialog.destroy()

                    else:
                        self.image_to_save.save(file_name)
                        self.encode_unsaved_changes = False
                        done = True
                        file_dialog.destroy()

                else:
                    done = True
                    file_dialog.destroy()

        else:
            self.encode_save_warning.set_text("There is nothing to save! Please encode a message to an image first.")

    def save_text(self, widget): # Save the decoded message as a .txt file

        if self.decode_func_run == True:
            done = False
            file_dialog = Gtk.FileChooserDialog(title="Save Text", parent=self, action=Gtk.FileChooserAction.SAVE)
            file_dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)

            filter = Gtk.FileFilter()
            filter.set_name(".txt")
            filter.add_pattern("*.txt")

            file_dialog.add_filter(filter)
            file_dialog.set_current_name(".txt")

            while done == False:

                file_response = file_dialog.run()

                if file_response == Gtk.ResponseType.OK:
                    file_name = file_dialog.get_filename()
                    if not file_name.endswith("txt"):
                        file_name += ".txt"

                    if exists(file_name):
                        save_dialog = Overwrite_Save(self)
                        save_response = save_dialog.run()

                        if save_response == Gtk.ResponseType.OK:
                            file = open(file_name, 'w')
                            file.write(self.decoded_message)
                            self.decode_unsaved_changes = False
                            done = True
                            file_dialog.destroy()
                        save_dialog.destroy()

                    else:
                        file = open(file_name, 'w')
                        file.write(self.decoded_message)
                        self.decode_unsaved_changes = False
                        done = True
                        file_dialog.destroy()

                else:
                    done = True
                    file_dialog.destroy()

        else:
            self.decode_save_warning.set_text("There is nothing to save! Please decode a message from an image first.")

    def reset_window(self): # Reset the Window to it's default state

        # Resetting the Encode tab

        self.encode_display_image.clear()
        self.max_char = 0
        self.max_char_label.set_text("Maxium characters: unknown")
        self.encode_image_label.set_text("Upload an image to update maximum character count")
        self.text_box_encode.set_editable(True)
        self.text_box_encode.set_cursor_visible(True)
        self.text_buffer_encode.set_text("Enter your message here or upload from a file")
        self.text_buffer_encode.set_modified(False)
        self.char_count_label.set_text("Character count: " + str(self.char_count))
        self.encode_image_uploaded = False
        self.encode_func_run = False
        self.final_display_image.clear()
        self.upload_warning_encode.set_text("")
        self.encode_save_warning.set_text("")
        self.text_file_contents = ""

        # Resetting the Decode tab

        self.decode_image_label = Gtk.Label(label="Actual image size: ?x?")
        self.decode_display_image.clear()
        self.text_buffer_decode.set_text("")
        self.decode_image_uploaded = False
        self.decode_func_run = False
        self.upload_warning_decode.set_text("")
        self.decode_save_warning.set_text("")

        self.encode_unsaved_changes = False
        self.decode_unsaved_changes = False

    def do_delete_event(self, event):

        if self.encode_unsaved_changes == True or self.decode_unsaved_changes == True:
            dialog = Unsaved_Dialog(self, "exit")
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                Gtk.main_quit()
                return False

            dialog.destroy()
            return True

        Gtk.main_quit()
        return False

class Unsaved_Dialog(Gtk.Dialog): # Popup window that will ask the user if they are sure they wish to exit or reset without saving

    def __init__(self, parent, exit_or_new):

        if exit_or_new == "exit":
            title = "Exit without saving?"
            label = "You have unsaved changes, are you sure you'd like to exit?"
        elif exit_or_new == "new":
            title = "Continue without saving?"
            label = "You have unsaved changes, are you sure you'd like to start a new project?"

        Gtk.Dialog.__init__(self, title, parent, modal=True)
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                         "Yes", Gtk.ResponseType.OK)

        self.set_default_size(200, 100)
        self.set_border_width(10)

        box = Gtk.Box()
        box.add(Gtk.Label(label=label))

        self.get_content_area().add(box)
        self.show_all()

class Overwrite_Save(Gtk.Dialog): # Popup window that will ask if user wants to overwrite an existing file when saveing

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Overwrite existing file?", parent, modal=True)
        self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                         "Yes", Gtk.ResponseType.OK)

        self.set_default_size(200, 100)
        self.set_border_width(10)

        box = Gtk.Box()
        box.add(Gtk.Label(label="A file already exists with that name, would you like to overwrite it?"))

        self.get_content_area().add(box)
        self.show_all()

class Non_ASCII(Gtk.Dialog):

    def __init__(self, parent):

        Gtk.Dialog.__init__(self, "Invalid message!", parent, modal=True)
        self.add_buttons("Okay", Gtk.ResponseType.OK)

        self.set_default_size(200, 100)
        self.set_border_width(10)

        box = Gtk.Box()
        box.add(Gtk.Label(label="Message can only contain ASCII characters!"))

        self.get_content_area().add(box)
        self.show_all()

window = MainWindow()
window.show_all()
Gtk.main()
