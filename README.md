# 🏝️ Creek Obhur Smart Management Dashboard

A smart AI-driven dashboard built for managing waterfront operations, based on real-time WhatsApp messages from supervisors and managers. Designed to help facility managers and shift supervisors efficiently track daily tasks, staff shifts, cleaning status, and safety incidents in a dynamic beachfront environment.

---

## 📌 Overview

This project was designed to streamline operations at the Creek Obhur waterfront facility by enabling automatic extraction of task data from WhatsApp messages and displaying it in a clean, structured, multi-section dashboard.

> ⚙️ Built with: **Streamlit**, **Python**, and (optionally) **NLP for message parsing**

---

## 🎯 Key Features

### 🧠 AI-Enhanced Task Capture *(optional module)*
- Receive **unstructured WhatsApp messages** from the manager.
- Automatically extract key task components: task type, location, assigned team, deadline.
- NLP-powered module using **Named Entity Recognition** (NER) and **Intent Classification**.

### 🧹 Toilets Cleaning Tracker
- Track cleaning time for each restroom (Male/Female).
- Record missing supplies or maintenance issues.
- Enable alerts for overdue cleaning tasks.

### 🏖️ Beach Supervision
- Overview of 3 separate beach zones.
- Display number of umbrellas, lifeguards, and assigned supervisors.
- Visual indicators for issues (missing staff, unattended zones).

### 👥 Staff Shifts Dashboard
- View who is currently on duty.
- Grouped by role (cleaners, lifeguards, supervisors, drivers).
- Upcoming shift rotation & absence reports.

### 📲 WhatsApp Integration (planned)
- Manager sends daily messages via WhatsApp.
- Tasks are extracted and assigned automatically (via backend NLP + webhook).
- No need to train non-technical users on new systems.

---

## 💡 Real-World Use Case

This system is currently used in a Saudi Arabian waterfront operations facility with:

- 🧑‍💼 17 supervisors and cashiers  
- 🧹 30+ cleaning staff  
- 🛟 10 lifeguards  
- 🧑‍✈️ 22 security staff  
- 🌴 3 beaches and 3 toilet blocks (each with male/female sections)

---

## 📦 Project Structure


