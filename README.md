# DIG for Windows 🔍

A modern, user-friendly GUI application for performing DNS lookups on Windows, built with PySide6. This tool serves as a graphical alternative to the traditional `dig` command, making DNS queries more accessible to Windows users.

## ✨ Features

- 🎨 Dark/Light mode support with automatic theme persistence
- 🌐 Support for multiple DNS record types (A, AAAA, MX, TXT, etc.)
- ⚡ Built-in popular DNS resolver options:
  - Cloudflare (1.1.1.1)
  - Google (8.8.8.8)
  - Hetzner (Multiple servers)
  - Quad9 (9.9.9.9)
  - System Default
- 📋 Clean and intuitive user interface
- 🔄 Asynchronous DNS queries (non-blocking UI)
- 📝 Query result logging with clear output formatting

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- PySide6
- dnspython

### Setup

1. Clone the repository:
```bash
git clone https://github.com/xfanexx/dig-for-windows.git
cd dig-for-windows
```

2. Install the required dependencies:
```bash
pip install PySide6 dnspython
```

3. Run the application:
```bash
python dig-for-windows.py
```

## 💡 Usage

1. **Select a DNS Server**: Choose from the predefined list of popular DNS servers or use your system's default.
2. **Enter Domain**: Type the domain name you want to query (e.g., "example.com").
3. **Choose Record Type**: Select the DNS record type from the dropdown menu.
4. **Perform Lookup**: Click the "Lookup" button to execute the query.
5. **View Results**: Results will be displayed in the text area below.
6. **Clear Log**: Use the "Clear Log" button to reset the results view.
7. **Toggle Theme**: Switch between dark and light modes using the theme toggle button.

## 🎯 Supported DNS Record Types

- ✅ A (IPv4 address)
- ✅ AAAA (IPv6 address)
- ✅ ANY (Any records)
- ✅ CAA (Certification Authority Authorization)
- ✅ CNAME (Canonical name)
- ✅ DNSKEY (DNS Key)
- ✅ DS (Delegation Signer)
- ✅ MX (Mail Exchange)
- ✅ NS (Name Server)
- ✅ PTR (Pointer)
- ✅ SOA (Start of Authority)
- ✅ SRV (Service)
- ✅ TLSA (TLSA)
- ✅ TSIG (Transaction Signature)
- ✅ TXT (Text)

## 🛠️ Technical Details

- Built with PySide6 (Qt for Python)
- Uses dnspython for DNS resolution
- Implements multithreading for non-blocking DNS queries
- Persistent settings storage using JSON
- Modern flat UI design with theme support

## 🔒 Error Handling

The application includes robust error handling for:
- Invalid domain names
- Network connectivity issues
- DNS resolution failures
- Timeouts
- Permission-related problems

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Known Issues

- Some DNS record types might not be supported by all DNS servers
- Theme switching might require application restart on some systems

## 🙏 Acknowledgments

- PySide6 team for the excellent Qt implementation
- dnspython developers for the robust DNS toolkit
- Various DNS providers for their public DNS services

---

Made with ❤️ for the Windows community
