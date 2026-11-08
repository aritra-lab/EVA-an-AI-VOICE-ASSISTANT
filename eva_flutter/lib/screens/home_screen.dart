import 'package:flutter/material.dart';

import '../widgets/sidebar.dart';
import '../widgets/top_bar.dart';
import '../widgets/chat_area.dart';
import '../widgets/voice_panel.dart';
import 'settings_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int selectedIndex = 0;

  final GlobalKey<EvaChatAreaState> chatKey =
      GlobalKey<EvaChatAreaState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF050816),
      body: Row(
        children: [
          EvaSidebar(
            selectedIndex: selectedIndex,
            onItemSelected: (index) {
              setState(() {
                selectedIndex = index;
              });
            },
          ),

          Expanded(
            child: selectedIndex == 0
                ? Column(
                    children: [
                      const EvaTopBar(),

                      Expanded(
                        child: EvaChatArea(
                          key: chatKey,
                        ),
                      ),

                      EvaVoicePanel(
                        onMessage: (message) {
                          chatKey.currentState?.sendMessage(
                            message,
                          );
                        },
                      ),
                    ],
                  )
                : const SettingsScreen(),
          ),
        ],
      ),
    );
  }
}