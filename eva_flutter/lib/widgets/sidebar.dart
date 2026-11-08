import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import 'eva_logo.dart';

class EvaSidebar extends StatelessWidget {
  final int selectedIndex;
  final ValueChanged<int> onItemSelected;

  const EvaSidebar({
    super.key,
    required this.selectedIndex,
    required this.onItemSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 270,
      decoration: const BoxDecoration(
        color: Color(0xFF080B20),
        border: Border(
          right: BorderSide(
            color: Color(0xFF252A50),
            width: 1,
          ),
        ),
      ),
      child: Column(
        children: [
          const SizedBox(height: 45),

          // ==========================================
          // EVA LOGO
          // ==========================================

          Container(
            width: 140,
            height: 140,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: const RadialGradient(
                colors: [
                  Color(0xFF21104D),
                  Color(0xFF090B22),
                ],
              ),
              border: Border.all(
                color: const Color(0xFF914FFF),
                width: 2,
              ),
              boxShadow: const [
                BoxShadow(
                  color: Color(0x668B4DFF),
                  blurRadius: 35,
                  spreadRadius: 6,
                ),
              ],
            ),
            child: const Center(
              child: CustomPaint(
                size: Size(100, 100),
                painter: EvaLogoPainter(),
              ),
            ),
          ),

          const SizedBox(height: 20),

          // ==========================================
          // HOLOGRAPHIC EVA TITLE
          // ==========================================

          ShaderMask(
            blendMode: BlendMode.srcIn,
            shaderCallback: (bounds) {
              return const LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  Color(0xFFFFFFFF),
                  Color(0xFFE7D7FF),
                  Color(0xFFB66CFF),
                  Color(0xFF7B5CFF),
                  Color(0xFFEDE8FF),
                ],
                stops: [
                  0.0,
                  0.25,
                  0.55,
                  0.78,
                  1.0,
                ],
              ).createShader(bounds);
            },
            child: Text(
              'EVA',
              style: GoogleFonts.orbitron(
                fontSize: 43,
                fontWeight: FontWeight.w500,
                letterSpacing: 10,
                height: 1,
              ),
            ),
          ),

          const SizedBox(height: 9),

          // ==========================================
          // EVA SUBTITLE
          // ==========================================

          Text(
            'ENHANCED VIRTUAL ASSISTANT',
            textAlign: TextAlign.center,
            style: GoogleFonts.spaceGrotesk(
              color: const Color(0xFF777C9E),
              fontSize: 9,
              fontWeight: FontWeight.w500,
              letterSpacing: 2.4,
            ),
          ),

          const SizedBox(height: 52),

          // ==========================================
          // CHAT
          // ==========================================

          GestureDetector(
            onTap: () => onItemSelected(0),
            child: Container(
              margin: const EdgeInsets.symmetric(
                horizontal: 16,
              ),
              height: 62,
              decoration: BoxDecoration(
                color: selectedIndex == 0
                    ? const Color(0xFF191342)
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: selectedIndex == 0
                      ? const Color(0xFF40357A)
                      : Colors.transparent,
                ),
                boxShadow: selectedIndex == 0
                    ? const [
                        BoxShadow(
                          color: Color(0x332E1B73),
                          blurRadius: 20,
                          spreadRadius: 1,
                        ),
                      ]
                    : null,
              ),
              child: Row(
                children: [
                  const SizedBox(width: 20),
                  const Icon(
                    Icons.chat_bubble_outline_rounded,
                    color: Color(0xFFB66CFF),
                    size: 27,
                  ),
                  const SizedBox(width: 18),
                  Text(
                    'Chat',
                    style: GoogleFonts.spaceGrotesk(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                      letterSpacing: 0.5,
                    ),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 15),

          // ==========================================
          // SETTINGS
          // ==========================================

          GestureDetector(
            onTap: () => onItemSelected(1),
            child: Container(
              margin: const EdgeInsets.symmetric(
                horizontal: 16,
              ),
              height: 58,
              decoration: BoxDecoration(
                color: selectedIndex == 1
                    ? const Color(0xFF191342)
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: selectedIndex == 1
                      ? const Color(0xFF40357A)
                      : Colors.transparent,
                ),
              ),
              child: Row(
                children: [
                  const SizedBox(width: 20),
                  const Icon(
                    Icons.settings_outlined,
                    color: Color(0xFF9A9DB8),
                    size: 26,
                  ),
                  const SizedBox(width: 18),
                  Text(
                    'Settings',
                    style: GoogleFonts.spaceGrotesk(
                      color: const Color(0xFF9A9DB8),
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                      letterSpacing: 0.4,
                    ),
                  ),
                ],
              ),
            ),
          ),

          const Spacer(),

          // ==========================================
          // ONLINE STATUS
          // ==========================================

          Container(
            margin: const EdgeInsets.symmetric(
              horizontal: 16,
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: 18,
              vertical: 16,
            ),
            decoration: BoxDecoration(
              color: const Color(0xFF0D1128),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: const Color(0x101F2850),
              ),
              boxShadow: const [
                BoxShadow(
                  color: Color(0x18000000),
                  blurRadius: 15,
                  spreadRadius: 1,
                ),
              ],
            ),
            child: Row(
              children: [
                const Icon(
                  Icons.circle,
                  size: 10,
                  color: Colors.greenAccent,
                ),
                const SizedBox(width: 11),
                Text(
                  'EVA Online',
                  style: GoogleFonts.spaceGrotesk(
                    color: Colors.white,
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                    letterSpacing: 0.4,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 25),
        ],
      ),
    );
  }
}