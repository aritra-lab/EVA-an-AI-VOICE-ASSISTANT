import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const EVA());
}

class EVA extends StatelessWidget {
  const EVA({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'EVA',
      home: const HomeScreen(),
    );
  }
}