# WebSocket Chat Server

This program is a WebSocket-based chat server written in Python. It allows multiple clients to connect and communicate with each other using the WebSocket protocol. The server also integrates with a banking service to process and respond to specific commands related to banking transactions and currency exchange rates.

## Installation
1. Clone the repository or download the source code files.
2. Open a terminal or command prompt and navigate to the directory where the program files are located.
3. Run the following command to install the project dependencies using Poetry:
   ```
   poetry install
   ```
   ```
   python server.py
   ```

5. The server will start running on `localhost` (127.0.0.1) and port `8080`.

## Usage

Once the server is running, clients can connect to it using a WebSocket client library or tool. Clients can send and receive messages to/from other connected clients.

### Connecting to the Server

To connect to the server, clients need to establish a WebSocket connection to `ws://localhost:8080`. The server will assign a random name to each connected client using the `names` library.

### Sending Messages

Clients can send messages to other connected clients by simply sending a text message over the WebSocket connection. The server will broadcast the message to all other clients.

### Banking Commands

The chat server also supports banking commands. If a client sends a message starting with the word "exchange", the server will process the command using the `bank` class from the `chat_commands` module. It will send a response to the client and broadcast the response to all other clients.

### Currency Exchange Rates

In addition to banking commands, the server can also retrieve currency exchange rates from the PrivatBank API. To use this feature, clients can send a message in the following format:

```
exchange <num_days> <currency>
```

- `<num_days>`: The number of previous days for which exchange rates should be retrieved (up to 10 days).
- `<currency>`: The currency code for which exchange rates are required.

For example, to get the exchange rates for the last 2 days for the currency KZT, a client can send the following message:

```
exchange 2 KZT
```

The server will process the command, retrieve the exchange rates, and send the response to the client. The response will also be broadcasted to all other connected clients.

### Logging

All executed commands are logged to a file called `chat_log.txt`. The log file is located in the `chat` directory.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request on the GitHub repository.

## License

This program is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and distribute it according to your needs.
