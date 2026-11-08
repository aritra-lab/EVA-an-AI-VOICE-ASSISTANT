import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'eva_logo.dart';

class EvaTopBar extends StatelessWidget {
  const EvaTopBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 86,
      decoration: const BoxDecoration(
        color: Color(0xFF070A1C),
        border: Border(
          bottom: BorderSide(
            color: Color(0xFF20264A),
            width: 1,
          ),
        ),
      ),
      child: Stack(
        children: [
          // ==========================================
          // HOLOGRAPHIC ACCENT LINE
          // ==========================================

          Positioned(
            left: 0,
            bottom: 0,
            child: Container(
              width: 360,
              height: 1,
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Color(0xFF5B2CFF),
                    Color(0xFF9D55FF),
                    Color(0xFF22CFFF),
                    Colors.transparent,
                  ],
                ),
              ),
            ),
          ),

          // ==========================================
          // HEADER CONTENT
          // ==========================================

          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: 40,
            ),
            child: Row(
              children: [
                // Small EVA lotus
                Container(
                  width: 38,
                  height: 38,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: Color(0x556B35FF),
                        blurRadius: 18,
                        spreadRadius: 2,
                      ),
                    ],
                  ),
                  child: const CustomPaint(
                    painter: EvaLogoPainter(),
                  ),
                ),

                const SizedBox(width: 18),

                // Greeting
                Text(
                  _greeting(),
                  style: GoogleFonts.orbitron(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.w500,
                    letterSpacing: 0.8,
                    shadows: const [
                      Shadow(
                        color: Color(0x665C6CFF),
                        blurRadius: 12,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _greeting() {
    final hour = DateTime.now().hour;

    if (hour >= 5 && hour < 12) {
      return 'Good Morning';
    }

    if (hour >= 12 && hour < 18) {
      return 'Good Afternoon';
    }

    return 'Good Evening';
  }
}