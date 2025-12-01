# src/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from .customer import CustomerRepo
from .table import TableRepo
from .reservation import ReservationRepo


class RestaurantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍽️ Restaurant Reservation System")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")

        title = tk.Label(
            self.root,
            text="Restaurant Reservation System",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )
        title.pack(pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.customer_tab = ttk.Frame(self.notebook)
        self.table_tab = ttk.Frame(self.notebook)
        self.reservation_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.customer_tab, text="Customers")
        self.notebook.add(self.table_tab, text="Tables")
        self.notebook.add(self.reservation_tab, text="Reservations")

        # Load UI
        self.build_customer_tab()
        self.build_table_tab()
        self.build_reservation_tab()

    # ============================
    # CUSTOMER TAB
    # ============================
    def build_customer_tab(self):
        frame = tk.Frame(self.customer_tab, pady=10)
        frame.pack()

        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Label(frame, text="Phone").grid(row=1, column=0)

        self.customer_name = tk.Entry(frame)
        self.customer_phone = tk.Entry(frame)

        self.customer_name.grid(row=0, column=1)
        self.customer_phone.grid(row=1, column=1)

        tk.Button(frame, text="Add Customer", command=self.add_customer).grid(
            row=2, column=0, columnspan=2, pady=6
        )
        tk.Button(frame, text="Update Customer", command=self.update_customer).grid(
            row=3, column=0, columnspan=2, pady=4
        )
        tk.Button(frame, text="Delete Customer", command=self.delete_customer).grid(
            row=4, column=0, columnspan=2, pady=4
        )

        self.customer_list = ttk.Treeview(
            self.customer_tab, columns=("id", "name", "phone"), show="headings", height=15
        )
        self.customer_list.pack(expand=True, fill="both", padx=8, pady=(6,12))

        for col in ("id", "name", "phone"):
            self.customer_list.heading(col, text=col.capitalize())

        # Bind selection to populate fields
        self.customer_list.bind("<<TreeviewSelect>>", self.on_customer_select)

        self.load_customers()

    def add_customer(self):
        name = self.customer_name.get().strip()
        phone = self.customer_phone.get().strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone required!")
            return

        try:
            CustomerRepo.create(name, phone)
            messagebox.showinfo("Success", "Customer added!")
            self.customer_name.delete(0, tk.END)
            self.customer_phone.delete(0, tk.END)
            self.load_customers()
            self.load_reservation_inputs()  # refresh combos
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_customer_select(self, _ev=None):
        sel = self.customer_list.selection()
        if not sel:
            return
        vals = self.customer_list.item(sel[0])["values"]
        # vals = (id, name, phone)
        self.customer_name.delete(0, tk.END)
        self.customer_name.insert(0, vals[1])
        self.customer_phone.delete(0, tk.END)
        self.customer_phone.insert(0, vals[2])

    def update_customer(self):
        sel = self.customer_list.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a customer to update!")
            return
        cid = int(self.customer_list.item(sel[0])["values"][0])
        name = self.customer_name.get().strip()
        phone = self.customer_phone.get().strip()
        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone required!")
            return
        try:
            CustomerRepo.update(cid, name, phone)
            messagebox.showinfo("Success", "Customer updated!")
            self.load_customers()
            self.load_reservation_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_customer(self):
        sel = self.customer_list.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a customer to delete!")
            return
        cid = int(self.customer_list.item(sel[0])["values"][0])
        if not messagebox.askyesno("Confirm", "Delete selected customer?"):
            return
        try:
            CustomerRepo.delete(cid)
            messagebox.showinfo("Success", "Customer deleted!")
            self.load_customers()
            self.load_reservation_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_customers(self):
        for row in self.customer_list.get_children():
            self.customer_list.delete(row)

        try:
            rows = CustomerRepo.list_all()
            for c in rows:
                self.customer_list.insert("", "end", values=(c["id"], c["name"], c["phone"]))
        except Exception as e:
            messagebox.showerror("Error", f"Load customers failed: {e}")

    # ============================
    # TABLE TAB
    # ============================
    def build_table_tab(self):
        frame = tk.Frame(self.table_tab, pady=10)
        frame.pack()

        tk.Label(frame, text="Table Number").grid(row=0, column=0)
        tk.Label(frame, text="Capacity").grid(row=1, column=0)

        self.table_number = tk.Entry(frame)
        self.table_capacity = tk.Entry(frame)

        self.table_number.grid(row=0, column=1)
        self.table_capacity.grid(row=1, column=1)

        tk.Button(frame, text="Add Table", command=self.add_table).grid(
            row=2, column=0, columnspan=2, pady=6
        )
        tk.Button(frame, text="Update Table", command=self.update_table).grid(
            row=3, column=0, columnspan=2, pady=4
        )
        tk.Button(frame, text="Delete Table", command=self.delete_table).grid(
            row=4, column=0, columnspan=2, pady=4
        )

        self.table_list = ttk.Treeview(
            self.table_tab,
            columns=("id", "number", "capacity", "status"),
            show="headings",
            height=15
        )
        self.table_list.pack(expand=True, fill="both", padx=8, pady=(6,12))

        for col in ("id", "number", "capacity", "status"):
            self.table_list.heading(col, text=col.capitalize())

        # Bind selection
        self.table_list.bind("<<TreeviewSelect>>", self.on_table_select)

        self.load_tables()

    def add_table(self):
        number = self.table_number.get().strip()
        capacity = self.table_capacity.get().strip()

        if not number or not capacity:
            messagebox.showwarning("Warning", "Table number and capacity required!")
            return

        try:
            TableRepo.create(number, capacity)
            messagebox.showinfo("Success", "Table added!")
            self.table_number.delete(0, tk.END)
            self.table_capacity.delete(0, tk.END)
            self.load_tables()
            self.load_reservation_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_table_select(self, _ev=None):
        sel = self.table_list.selection()
        if not sel:
            return
        vals = self.table_list.item(sel[0])["values"]
        # vals = (id, number, capacity, status)
        self.table_number.delete(0, tk.END)
        self.table_number.insert(0, vals[1])
        self.table_capacity.delete(0, tk.END)
        self.table_capacity.insert(0, vals[2])

    def update_table(self):
        sel = self.table_list.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a table to update!")
            return
        tid = int(self.table_list.item(sel[0])["values"][0])
        number = self.table_number.get().strip()
        capacity = self.table_capacity.get().strip()
        if not number or not capacity:
            messagebox.showwarning("Warning", "Number and capacity required!")
            return
        try:
            # preserve status from treeview if present
            status = self.table_list.item(sel[0])["values"][3] if len(self.table_list.item(sel[0])["values"]) > 3 else "available"
            TableRepo.update(tid, number, capacity, status)
            messagebox.showinfo("Success", "Table updated!")
            self.load_tables()
            self.load_reservation_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_table(self):
        sel = self.table_list.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a table to delete!")
            return
        tid, number, cap, status = self.table_list.item(sel[0])["values"]
        if status == "booked":
            messagebox.showwarning("Warning", "Can't delete a booked table!")
            return
        if not messagebox.askyesno("Confirm", f"Delete table {number}?"):
            return
        try:
            TableRepo.delete(int(tid))
            messagebox.showinfo("Success", "Table deleted!")
            self.load_tables()
            self.load_reservation_inputs()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_tables(self):
        for row in self.table_list.get_children():
            self.table_list.delete(row)

        try:
            rows = TableRepo.list_all()
            for t in rows:
                # ensure keys names consistent with repo (number or table_number)
                number = t.get("number") or t.get("table_number")
                status = t.get("status") or "available"
                self.table_list.insert("", "end", values=(t["id"], number, t["capacity"], status))
        except Exception as e:
            messagebox.showerror("Error", f"Load tables failed: {e}")

    # ============================
    # RESERVATION TAB
    # ============================
    def load_reservation_inputs(self):
        try:
            customers = CustomerRepo.list_all()
            self.customer_combo['values'] = [f"{c['id']} - {c['name']}" for c in customers]
        except Exception:
            self.customer_combo['values'] = []

        # Load available tables only
        try:
            tables = TableRepo.list_all()
            available_tables = [t for t in tables if t.get('status', 'available') == 'available']
            self.table_combo['values'] = [f"{t['id']} - Table {t['number']}" for t in available_tables]
        except Exception:
            self.table_combo['values'] = []
            
    def build_reservation_tab(self):
        frame = tk.Frame(self.reservation_tab, pady=10)
        frame.pack()

        # Customer choose
        tk.Label(frame, text="Customer").grid(row=0, column=0)
        self.customer_combo = ttk.Combobox(frame, width=25)
        self.customer_combo.grid(row=0, column=1)

        # Table choose (available only)
        tk.Label(frame, text="Table (Available)").grid(row=1, column=0)
        self.table_combo = ttk.Combobox(frame, width=25)
        self.table_combo.grid(row=1, column=1)

        # Date
        tk.Label(frame, text="Date").grid(row=2, column=0)
        self.date_entry = DateEntry(frame, width=25)
        self.date_entry.grid(row=2, column=1)

        # Time
        tk.Label(frame, text="Time (HH:MM)").grid(row=3, column=0)
        self.time_entry = tk.Entry(frame)
        self.time_entry.grid(row=3, column=1)
        self.time_entry.insert(0, "19:00")

        # Tombol Create
        tk.Button(frame, text="Create Reservation", command=self.create_reservation).grid(
            row=4, column=0, columnspan=2, pady=6
        )

        # Tombol Update dan Delete
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=4)

        tk.Button(btn_frame, text="Update Reservation", command=self.update_reservation).grid(row=0, column=0, padx=4)
        tk.Button(btn_frame, text="Delete Reservation", command=self.cancel_reservation).grid(row=0, column=1, padx=4)

        # Treeview daftar reservation
        self.reservation_list = ttk.Treeview(
            self.reservation_tab,
            columns=("id", "customer", "table", "date", "time"),
            show="headings",
            height=12
        )
        self.reservation_list.pack(expand=True, fill="both", padx=8, pady=(6,6))

        for col in ("id", "customer", "table", "date", "time"):
            self.reservation_list.heading(col, text=col.capitalize())

        # Bind selection to pre-select values
        self.reservation_list.bind("<<TreeviewSelect>>", self.on_reservation_select)


        # Load data
        self.load_reservations()
        self.load_reservation_inputs()


    def create_reservation(self):
        try:
            customer_id = int(self.customer_combo.get().split(" - ")[0])
            table_id = int(self.table_combo.get().split(" - ")[0])
        except Exception:
            messagebox.showwarning("Warning", "Select customer and table!")
            return

        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        time = self.time_entry.get().strip()
        if not time:
            messagebox.showwarning("Warning", "Enter time!")
            return

        try:
            rid = ReservationRepo.create(customer_id, table_id, date, time)
            # set_booked may be called inside repo.create or here depending on your repo implementation
            try:
                TableRepo.set_booked(table_id)
            except Exception:
                pass
            messagebox.showinfo("Success", f"Reservation created! (id={rid})")
            self.load_reservations()
            self.load_reservation_inputs()
            self.load_tables()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_reservation_select(self, _ev=None):
        sel = self.reservation_list.selection()
        if not sel:
            return
        vals = self.reservation_list.item(sel[0])["values"]
        # vals = (id, customer_name, table_number, date, time)
        # try to preselect customer and table in comboboxes
        customer_name = vals[1]
        table_number = vals[2]
        date = vals[3]
        time = vals[4]

        # select matching customer entry in combobox if exists
        try:
            customers = self.customer_combo["values"]
            match = next((v for v in customers if v.endswith(f" - {customer_name}") or v.split(" - ")[1] == customer_name), None)
            if match:
                self.customer_combo.set(match)
        except Exception:
            pass

        # select matching table entry in combobox if exists
        try:
            tables = self.table_combo["values"]
            match = next((v for v in tables if v.endswith(f"Table {table_number}") or v.split(" - ")[1].strip().endswith(str(table_number))), None)
            if match:
                self.table_combo.set(match)
        except Exception:
            pass

        try:
            # set date and time fields
            self.date_entry.set_date(datetime.strptime(date, "%Y-%m-%d").date())
        except Exception:
            pass
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, time)

    def load_reservations(self):
        for row in self.reservation_list.get_children():
            self.reservation_list.delete(row)

        try:
            rows = ReservationRepo.list_all()
            for r in rows:
                # r expected to contain keys: id, customer_name, table_number, date, time
                self.reservation_list.insert(
                    "", "end",
                    values=(r["id"], r.get("customer_name") or r.get("customer_id"), r.get("table_number") or r.get("table_id"), r.get("date"), r.get("time"))
                )
        except Exception as e:
            messagebox.showerror("Error", f"Load reservations failed: {e}")

    def update_reservation(self):
        sel = self.reservation_list.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a reservation to update!")
            return
        rid = int(self.reservation_list.item(sel[0])["values"][0])

        try:
            customer_id = int(self.customer_combo.get().split(" - ")[0])
            new_table_id = int(self.table_combo.get().split(" - ")[0])
        except Exception:
            messagebox.showwarning("Warning", "Select customer and table!")
            return

        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        time = self.time_entry.get().strip()

        try:
            # get old table id to free it (if different)
            old_table_number = self.reservation_list.item(sel[0])["values"][2]
            old_table_id = TableRepo.get_id_by_number(old_table_number)

            # update reservation
            ReservationRepo.update(rid, customer_id, new_table_id, date, time)

            # free old table if it's different and not None
            try:
                if old_table_id and old_table_id != new_table_id:
                    TableRepo.set_available(old_table_id)
            except Exception:
                pass

            # set new table booked
            try:
                TableRepo.set_booked(new_table_id)
            except Exception:
                pass

            messagebox.showinfo("Success", "Reservation updated!")
            self.load_reservations()
            self.load_reservation_inputs()
            self.load_tables()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_reservation(self):
        selected = self.reservation_list.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a reservation to cancel!")
            return

        rid, _, table_number, _, _ = self.reservation_list.item(selected)["values"]

        # get table id by number (supports repo implementation)
        try:
            table_id = TableRepo.get_id_by_number(table_number)
        except Exception:
            # fallback: if table_number is actually an id string
            try:
                table_id = int(table_number)
            except Exception:
                table_id = None

        if not messagebox.askyesno("Confirm", "Cancel this reservation?"):
            return

        try:
            ReservationRepo.cancel(int(rid))
            if table_id:
                try:
                    TableRepo.set_available(table_id)
                except Exception:
                    pass
            messagebox.showinfo("Success", "Reservation cancelled!")
            self.load_reservations()
            self.load_reservation_inputs()
            self.load_tables()
        except Exception as e:
            messagebox.showerror("Error", str(e))


