'''
This is the final shopping list project.
I know I could have made the interface a little nicer, but it was too annoying.
Click "Create New" to add an item to the list.
If the item is surrounded by a red colour, there is an error.
An item with an error will not be calculated.
You can also add a tax at the bottom bar (the default is 0%).
The bottom bar will return the total # of items and the total price with tax.
'''

# *This version might be the last one where I store data and can calculate the total cost.
# *I also will make tweeks of framework design after I finish.
from tkinter import *
root = Tk()
root.title("Shopping List")

# ?I think I need to use an __init__ so that because I need to use the bottom_frame in following functions too
# ?I don't think it will create a big mess but we will see.


class FrameWork:
    # * I will avoid naming this __init__ since I don't want it to affect all the other functions
    CURRENT_ROW = 1
    ITEM_LIST = []
    # *Bottom Frame
    # Somehow things work more smoothly when I don't put this in the __init__ method.
    bottom_frame = LabelFrame(root)
    bottom_total = Label(
        bottom_frame, text="TOTAL", padx=30, relief="ridge")
    bottom_total.grid(row=0, column=0)
    bottom_tax_label = Label(
        bottom_frame, text="Tax: ")
    bottom_tax_label.grid(row=0, column=1)
    bottom_tax_entry = Entry(
        bottom_frame, width=5, borderwidth=5)
    bottom_tax_entry.insert(0, "0")
    bottom_tax_entry.grid(row=0, column=2)
    bottom_tax_per = Label(bottom_frame, text="%")
    bottom_tax_per.grid(row=0, column=3)
    bottom_number = Label(
        bottom_frame, text="(Total # of Items)", width=13, relief="ridge")
    bottom_number.grid(row=0, column=4)
    bottom_price = Label(
        bottom_frame, text="(Total Price)", width=10, relief="ridge")
    bottom_price.grid(row=0, column=5)
    print_total = Button(
        bottom_frame, text="Print Total", width=30, fg="red", command=lambda: FinalCalc(root))
    print_total.grid(row=0, column=6)

    def __init__(self, root):
        # * Title Frame
        self.title_frame = LabelFrame(root)
        self.create_new = Button(
            #!Might have to change where things redirect to.
            #!The thing is that
            self.title_frame, text="Create New Item", fg="red", command=lambda: Create(root))
        self.create_new.grid(row=0, column=0)
        self.price_label = Label(
            self.title_frame, text="Price Per Item\n(Dollars . Cents)", relief="ridge")
        self.price_label.grid(row=0, column=1)
        self.number_of_items = Label(
            self.title_frame, text="Number of Items", relief="ridge")
        self.number_of_items.grid(row=0, column=2)
        self.total_label = Label(
            self.title_frame, text="Subtotal", relief="ridge", padx=13)
        self.total_label.grid(row=0, column=3)
        self.options = Label(
            self.title_frame, text="Options", relief="ridge", padx=17)
        self.options.grid(row=0, column=4)
        self.status_label = Label(
            self.title_frame, text="Error", relief="ridge", width=20)
        self.status_label.grid(row=0, column=5)
        # title_frame.grid(row=0, column=0)

    def permanent(self, root):
        self.title_frame.grid(row=0, column=0, sticky=W)
        # self.bottom_frame.grid(row=1, column=0)

    def temporary(self, root):
        # ?Even though I initialized the bottom frame, somehow frame doesn't work.
        # ?It might be because of the way I was calling it but I honestly don't know.
        # *I fixed this by making the bottom frame a class attribute. Hope this doesn't mess things up in the future.
        #!I will try putting frame outside of the init
        FrameWork.bottom_frame.grid_forget()
        FrameWork.bottom_frame.grid(
            row=FrameWork.CURRENT_ROW + 1, column=0, sticky=W)


# ?Question 1: Does Create have to inherit from Framework?
# *My current answer: No, since Create doesn't involve any widgets made in Framework, though it calls functions from it.


class Create(FrameWork):
    def __init__(self, root):
        # *Green yellow is a good colour for correct format.
        self.item_frame = LabelFrame(root, bg="red")
        self.item_frame.bind("<Enter>", self.hover_on_before)
        self.item_frame.bind("<Leave>", self.hover_out_before)
        self.item_name_entry = Entry(self.item_frame, width=15, borderwidth=5)
        self.item_name_entry.grid(row=0, column=0)
        self.dollar_sign = Label(self.item_frame, text="$")
        self.dollar_sign.grid(row=0, column=1)
        self.dollar_entry = Entry(self.item_frame, width=3, borderwidth=7)
        self.dollar_entry.grid(row=0, column=2)
        self.dot_label = Label(self.item_frame, text=".")
        self.dot_label.grid(row=0, column=3)
        self.cents_entry = Entry(self.item_frame, width=3, borderwidth=7)
        self.cents_entry.grid(row=0, column=4)
        self.number_entry = Entry(self.item_frame, width=14, borderwidth=5)
        self.number_entry.grid(row=0, column=5)
        self.subtotal_label = Label(
            self.item_frame, text="", relief="ridge", width=12)
        self.subtotal_label.grid(row=0, column=6)
        self.replace_label = Label(self.item_frame, text="", width=10)
        self.replace_label.grid(row=0, column=7)
        self.status_notice = Label(
            self.item_frame, text="Item has not been added.", fg="red", width=22)
        self.status_notice.grid(row=0, column=8)
        self.item_frame.grid(row=FrameWork.CURRENT_ROW, column=0, sticky=W)
        FrameWork.temporary(self, root)
        FrameWork.CURRENT_ROW += 1

    #!might have to use the unbinding function to change binding.
    # *Based on the previous example, key bindings don't run the __init__ method
    def hover_on_before(self, event):
        self.replace_label.grid_forget()
        self.status_notice.grid_forget()
        #!Passing self is a BIG SUCCESS because it doesn't call the __init__ function!!
        self.button1 = Button(self.item_frame, text="Add",
                              command=lambda: Save.add_value(self, root))
        self.button1.grid(row=0, column=8)
        self.button2 = Button(self.item_frame, text="Delete",
                              command=lambda: Save.delete_value(self, root))
        self.button2.grid(row=0, column=9)
        self.status_notice.grid(row=0, column=10)

    def hover_on_add(self, event):
        self.replace_label.grid_forget()
        self.button1 = Button(self.item_frame, text="Edit",
                              command=lambda: Save.edit_value(self, root))
        self.button1.grid(row=0, column=7)
        self.button2.grid(row=0, column=8)

    def hover_on_edit(self, event):
        self.replace_label.grid_forget()
        self.button1 = Button(self.item_frame, text="Save",
                              command=lambda: Save.save_value(self, root), width=3)
        self.button1.grid(row=0, column=7)
        self.button2.grid(row=0, column=8)

    def hover_out_before(self, event):
        self.button1.grid_forget()
        self.button2.grid_forget()
        self.replace_label.grid(row=0, column=8)


# * I have to make sure the changed binding will not call the __init__ method, so be careful.


class Save:
    def add_value(self, root):
        self.object = StoreInfo(root, self.item_name_entry.get(),
                                self.dollar_entry.get(), self.cents_entry.get(), self.number_entry.get())

        # *Forget everything
        # ?It seems like if I am on the frame from the beginning, the "<Enter>" binding doesn't work.
        self.item_frame.unbind("<Enter>")
        self.item_frame.bind("<Enter>", self.hover_on_add)
        self.item_name_entry.grid_forget()
        self.dollar_sign.grid_forget()
        self.dollar_entry.grid_forget()
        self.dot_label.grid_forget()
        self.cents_entry.grid_forget()
        self.number_entry.grid_forget()
        self.subtotal_label.grid_forget()
        self.button1.grid_forget()
        self.button2.grid_forget()
        self.status_notice.grid_forget()

        # *Recreate
        self.item_name_label = Label(
            self.item_frame, text=self.item_name_entry.get(), relief="ridge", width=14, pady=3.5)
        self.item_name_label.grid(row=0, column=0)
        self.dollar_sign.grid(row=0, column=1)
        self.dollar_label = Label(
            self.item_frame, text=self.dollar_entry.get(), width=3)
        self.dollar_label.grid(row=0, column=2, sticky=E)
        self.dot_label.grid(row=0, column=3)
        #!Must make this change for the save version too.
        self.cents_label = Label(
            self.item_frame, text=self.object.show_cents, width=3)
        self.cents_label.grid(row=0, column=4)
        self.number_label = Label(
            self.item_frame, text=self.number_entry.get(), relief="ridge", width=13)
        self.number_label.grid(row=0, column=5)
        self.subtotal_label.grid(row=0, column=6)
        self.button1 = Button(self.item_frame, text="Edit",
                              command=lambda: Save.edit_value(self, root))
        self.button1.grid(row=0, column=7)
        self.button2.grid(row=0, column=8)

        self.status_notice.config(
            text=self.object.status, fg=self.object.notice_colour)
        self.status_notice.grid(row=0, column=9)
        self.item_frame.config(bg=self.object.status_colour)
        # *for the purpose of saving when the object failed the initial test,
        # *I think I should add the object to the list anyway and I can filter using self.status
        self.subtotal_label.config(text=self.object.show_subtotal)
        FrameWork.ITEM_LIST += [self.object]


    def edit_value(self, root):
        # *Forget everything
        self.item_frame.unbind("<Enter>")
        self.item_frame.bind("<Enter>", self.hover_on_edit)
        self.item_name_label.grid_forget()
        self.dollar_sign.grid_forget()
        self.dollar_label.grid_forget()
        self.dot_label.grid_forget()
        self.cents_label.grid_forget()
        self.number_label.grid_forget()
        self.subtotal_label.grid_forget()
        self.button1.grid_forget()
        self.button2.grid_forget()

        # *Recreate
        # The entry stores the stuff entered, so I can just
        # slap it on the screen again.
        self.item_name_entry.grid(row=0, column=0)
        self.dollar_sign.grid(row=0, column=1)
        self.dollar_entry.grid(row=0, column=2)
        self.dot_label.grid(row=0, column=3)
        #!I am going to insert cents_entry with the modified cents
        self.cents_entry = Entry(self.item_frame, width=3, borderwidth=7)
        self.cents_entry.insert(0, self.object.show_cents)
        self.cents_entry.grid(row=0, column=4)
        self.number_entry.grid(row=0, column=5)
        self.subtotal_label.grid(row=0, column=6)
        self.replace_label.config(padx=0)
        #self.replace_label.grid(row=0, column=7)
        #!As for the last example, since the cursor is on the frame for default,
        #!I have to add the button for default
        self.button1 = Button(self.item_frame, text="Save",
                              command=lambda: Save.save_value(self, root), width=3)
        self.button1.grid(row=0, column=7)
        self.button2.grid(row=0, column=8)

    def save_value(self, root):
        # *Forget Everything
        self.item_frame.unbind("<Enter>")
        self.item_frame.bind("<Enter>", self.hover_on_add)
        self.item_name_entry.grid_forget()
        self.dollar_sign.grid_forget()
        self.dollar_entry.grid_forget()
        self.dot_label.grid_forget()
        self.cents_entry.grid_forget()
        self.number_entry.grid_forget()
        self.subtotal_label.grid_forget()
        self.button1.grid_forget()
        self.button2.grid_forget()
        # Guess .get() doesn't update all the time.
        # *I have to re-get all the info
        self.item_name_label.config(text=self.item_name_entry.get())
        self.item_name_label.grid(row=0, column=0)
        self.dollar_sign.grid(row=0, column=1)
        self.dollar_label.config(text=self.dollar_entry.get())
        self.dollar_label.grid(row=0, column=2)
        self.dot_label.grid(row=0, column=3)
        #!Since the cents label can change, I placed it after I pass it through StoreInfo
        self.number_label.config(text=self.number_entry.get())
        self.number_label.grid(row=0, column=5)
        self.subtotal_label.grid(row=0, column=6)
        self.button1 = Button(self.item_frame, text="Edit",
                              command=lambda: Save.edit_value(self, root))
        self.button1.grid(row=0, column=7)
        self.button2.grid(row=0, column=8)

        # *Gotta make checking work for saving too
        # *using the .insert() method
        #!I have to make sure to run the test again.
        #!I also have to consider the possibility that the object failed the initial test.
        self.index = FrameWork.ITEM_LIST.index(self.object)
        FrameWork.ITEM_LIST.remove(self.object)
        self.object = StoreInfo(root, self.item_name_entry.get(),
                                self.dollar_entry.get(), self.cents_entry.get(), self.number_entry.get())
        FrameWork.ITEM_LIST.insert(self.index, self.object)
        self.subtotal_label.config(text=self.object.show_subtotal)
        self.item_frame.config(bg=self.object.status_colour)
        self.status_notice.config(
            text=self.object.status, fg=self.object.notice_colour)
        self.cents_label.config(text=self.object.show_cents)
        self.cents_label.grid(row=0, column=4)


    def delete_value(self, root):
        self.item_frame.grid_forget()
        # *That was honestly pretty simple but I have to add some data features here.
        # *This is for when the item has not been added to the list.
        try:
            FrameWork.ITEM_LIST.remove(self.object)
        except ValueError:
            pass
        except AttributeError:
            pass



class StoreInfo:
    def __init__(self, root, name, dollars, cents, number):
        # * I should make an error holder to display any errors that occured
        # *I think this can be done in strings with a \n
        # *I should change the background colour of the status bar
        # *Red for error, light green for correct
        #!Since this is at the point of adding the object,
        #!I can first assume that it is good to go.
        # *Instead of assigning an initial I can check whether a value was assigned
        # *by "if self.status"
        #!But, I need an initial value to start off
        self.status_colour = "red"
        self.notice_colour = "red"
        if len(name) == 0:
            self.name = "Name Error"
            self.status = "Item name cannot be empty."
        else:
            self.name = name

        dollar_checker = False
        for i in dollars:
            if str(i).isdigit():
                dollar_checker = True
            else:
                dollar_checker = False
                break
        if dollar_checker == False:
            self.price = "Price Error"
            self.show_cents = cents

        if len(cents) == 0:
            try:
                self.price = format(float(dollars), '.2f')
                self.show_cents = "00"
            except ValueError:
                self.show_cents = cents
                self.price = "Price Error"
                try:
                    self.status += f"\n{dollars}.{cents} is an invalid price."
                except AttributeError:
                    self.status = f"{dollars}.{cents} is an invalid price."
        elif len(cents) == 1:
            try:
                self.show_cents = round(float(cents) * 10)
                self.new_cents = float(cents) / 10
                self.price = format(float(dollars) + self.new_cents, '.2f')
            except ValueError:
                self.show_cents = cents
                self.price = "Price Error"
                try:
                    self.status += f"\n{dollars}.{cents} is an invalid price."
                except AttributeError:
                    self.status = f"{dollars}.{cents} is an invalid price."
        elif len(cents) == 2:
            # *The self.price is correct but the showing is inaccurate
            # *I need to fix the show_cents part
            try:
                self.new_cents = float(cents) / 100
                self.price = format(float(dollars) + self.new_cents, '.2f')
                self.show_cents = str(self.price[-2:])
            except ValueError:
                self.show_cents = cents
                self.price = "Price Error"
                try:
                    self.status += f"\n{dollars}.{cents} is an invalid price."
                except AttributeError:
                    self.status = f"{dollars}.{cents} is an invalid price."
        else:
            self.show_cents = cents
            self.price = "Price Error"
            try:
                self.status += f"\n{dollars}.{cents} is an invalid price."
            except AttributeError:
                self.status = f"{dollars}.{cents} is an invalid price."

        int_checker = False
        for i in number:
            if str(i).isdigit():
                int_checker = True
            else:
                int_checker = False
                break

        if int_checker:
            self.number = int(number)
        else:
            self.number = "Number Error"
            try:
                self.status += f"\n# of items '{number}' is not an integer."
            except AttributeError:
                self.status = f"# of items '{number}' is not an integer."

        try:
            if self.status:
                self.actual_subtotal = ""
                self.show_subtotal = ""
        except AttributeError:
            self.status = ""
            self.status_colour = "green yellow"
            self.notice_colour = "black"
            self.actual_subtotal = format(
                float(self.price) * int(self.number), ".2f")
            self.show_subtotal = "$ " + \
                format(float(self.price) * int(self.number), ".2f")
# ?This is difficult to make it work.
# *I have to find a way to pass in the tax varibale too.


class FinalCalc:
    def __init__(self, root):
        self.item_total = 0
        self.price_total = 0
        for i in FrameWork.ITEM_LIST:
            if i.status == "":
                self.item_total += i.number
                self.price_total += float(i.actual_subtotal)
        self.price_total = self.price_total * \
            (1 + (float(FrameWork.bottom_tax_entry.get())) / 100)
        self.price_total = "$ " + str(format(self.price_total, '.2f'))
        FrameWork.bottom_number.config(text=self.item_total)
        FrameWork.bottom_price.config(text=self.price_total)


b = FrameWork(root)
b.permanent(root)
mainloop()
