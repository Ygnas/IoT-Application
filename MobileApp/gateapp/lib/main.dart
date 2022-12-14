import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:firebase_storage/firebase_storage.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  final channel = WebSocketChannel.connect(
    Uri.parse('ws://192.168.0.138:8000'),
  );

  final textController = TextEditingController();

  void dispose() {
    channel.sink.close();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.deepPurple[300],
        body: StreamBuilder(
          stream: channel.stream,
          builder: (context, snapshot) {
            textController.text =
                snapshot.hasData ? '${snapshot.data}' : 'Server is Offline';
            return Column(children: [
              const SizedBox(
                height: 350,
              ),
              Center(
                child: Text(
                  textController.text,
                  style: const TextStyle(fontSize: 25),
                ),
              ),
              const SizedBox(
                height: 50,
              ),
              Container(
                child: textController.text == "Can Be Opened"
                    ? FloatingActionButton.extended(
                        onPressed: () {
                          if (textController.text == "Can Be Opened") {
                            channel.sink.add('open');
                          }
                        },
                        label: const Text("Open Gate"),
                        icon: const Icon(Icons.lock_open_rounded),
                      )
                    : FloatingActionButton.extended(
                        onPressed: () {
                          if (textController.text == "Can Be Opened") {
                            channel.sink.add('open');
                          }
                        },
                        label: const Text("🤯"),
                        icon: const Icon(Icons.lock_rounded),
                        backgroundColor: Colors.red,
                      ),
              ),
            ]);
          },
        ),
      ),
    );
  }
}
