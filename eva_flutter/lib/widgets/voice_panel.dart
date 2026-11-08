import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../services/eva_api.dart';

class EvaVoicePanel extends StatefulWidget {
  final Function(String) onMessage;

  const EvaVoicePanel({
    super.key,
    required this.onMessage,
  });

  @override
  State<EvaVoicePanel> createState() => _EvaVoicePanelState();
}

class _EvaVoicePanelState extends State<EvaVoicePanel>
    with SingleTickerProviderStateMixin {
  bool isListening = false;
  String recognizedText = '';

  late AnimationController pulseController;

  @override
  void initState() {
    super.initState();

    pulseController = AnimationController(
      vsync: this,
      duration: const Duration(
        milliseconds: 1800,
      ),
    );
  }

  Future<void> toggleListening() async {
    if (isListening) {
      return;
    }

    setState(() {
      isListening = true;
      recognizedText = '';
    });

    pulseController.repeat();

    try {
      final command = await EvaApi.listen();

      if (command.isNotEmpty) {
        widget.onMessage(command);
      }

      if (mounted) {
        setState(() {
          recognizedText = command;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          recognizedText =
              'Could not connect to EVA speech service.';
        });
      }
    } finally {
      pulseController.stop();
      pulseController.reset();

      if (mounted) {
        setState(() {
          isListening = false;
        });
      }
    }
  }

  @override
  void dispose() {
    pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          margin: const EdgeInsets.fromLTRB(
            45,
            0,
            45,
            8,
          ),
          height: 165,
          width: double.infinity,
          decoration: BoxDecoration(
            color: const Color(0xFF080C22),
            borderRadius: BorderRadius.circular(25),
            border: Border.all(
              color: const Color(0xFF252B55),
            ),
            boxShadow: const [
              BoxShadow(
                color: Color(0x14000000),
                blurRadius: 30,
                spreadRadius: 2,
              ),
            ],
          ),
          child: Stack(
            children: [
              // ==========================================
              // AMBIENT CENTER GLOW
              // ==========================================

              AnimatedPositioned(
                duration: const Duration(
                  milliseconds: 500,
                ),
                curve: Curves.easeInOutCubic,
                top: isListening ? 35 : 15,
                left: 0,
                right: 0,
                child: AnimatedContainer(
                  duration: const Duration(
                    milliseconds: 500,
                  ),
                  width: isListening ? 180 : 130,
                  height: isListening ? 180 : 130,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: RadialGradient(
                      colors: [
                        Color(0x443F1B9A),
                        Color(0x221B4DFF),
                        Colors.transparent,
                      ],
                    ),
                  ),
                ),
              ),

              // ==========================================
              // LISTENING TEXT
              // ==========================================

              AnimatedPositioned(
                duration: const Duration(
                  milliseconds: 400,
                ),
                curve: Curves.easeInOutCubic,
                top: isListening ? 14 : 2,
                left: 30,
                right: 30,
                child: AnimatedOpacity(
                  duration: const Duration(
                    milliseconds: 250,
                  ),
                  opacity: isListening ? 1 : 0,
                  child: ShaderMask(
                    blendMode: BlendMode.srcIn,
                    shaderCallback: (bounds) {
                      return const LinearGradient(
                        begin: Alignment.centerLeft,
                        end: Alignment.centerRight,
                        colors: [
                          Color(0xFF8D6CFF),
                          Color(0xFFD19CFF),
                          Color(0xFF6F8CFF),
                        ],
                      ).createShader(bounds);
                    },
                    child: Text(
                      recognizedText.isEmpty
                          ? 'LISTENING'
                          : recognizedText,
                      textAlign: TextAlign.center,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: GoogleFonts.spaceGrotesk(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        letterSpacing: 2.5,
                        shadows: const [
                          Shadow(
                            color: Color(0x885F36FF),
                            blurRadius: 14,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),

              // ==========================================
              // HOLOGRAPHIC RING + MICROPHONE
              // ==========================================

              AnimatedPositioned(
                duration: const Duration(
                  milliseconds: 450,
                ),
                curve: Curves.easeInOutCubic,
                top: isListening ? 70 : 40,
                left: 0,
                right: 0,
                child: Center(
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      // ==================================
                      // OUTER PULSE RING
                      // ==================================

                      AnimatedBuilder(
                        animation: pulseController,
                        builder: (context, child) {
                          final pulse =
                              pulseController.value;

                          return Container(
                            width: isListening
                                ? 125 + (pulse * 18)
                                : 112,
                            height: isListening
                                ? 125 + (pulse * 18)
                                : 112,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: const Color(
                                  0x335F4BFF,
                                ),
                                width: 1.5,
                              ),
                            ),
                          );
                        },
                      ),

                      // ==================================
                      // MICROPHONE CORE
                      // ==================================

                      GestureDetector(
                        onTap: toggleListening,
                        child: AnimatedContainer(
                          duration: const Duration(
                            milliseconds: 350,
                          ),
                          curve: Curves.easeInOutCubic,
                          width: isListening ? 86 : 84,
                          height: isListening ? 86 : 84,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: const RadialGradient(
                              colors: [
                                Color(0xFF24175C),
                                Color(0xFF111034),
                              ],
                            ),
                            border: Border.all(
                              color: isListening
                                  ? const Color(
                                      0xFFB66CFF,
                                    )
                                  : const Color(
                                      0xFF9D55FF,
                                    ),
                              width: 2.5,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: const Color(
                                  0x889D55FF,
                                ),
                                blurRadius:
                                    isListening
                                        ? 42
                                        : 28,
                                spreadRadius:
                                    isListening
                                        ? 8
                                        : 4,
                              ),
                              const BoxShadow(
                                color: Color(
                                  0x3329C8FF,
                                ),
                                blurRadius: 20,
                                spreadRadius: 2,
                              ),
                            ],
                          ),
                          child: Icon(
                            isListening
                                ? Icons.stop_rounded
                                : Icons.mic_rounded,
                            size: 37,
                            color: const Color(
                              0xFF42C8FF,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),

        // ==========================================
        // HOLOGRAPHIC SPEAK LABEL
        // ==========================================

        Padding(
          padding: const EdgeInsets.only(
            bottom: 12,
            top: 4,
          ),
          child: ShaderMask(
            blendMode: BlendMode.srcIn,
            shaderCallback: (bounds) {
              return const LinearGradient(
                begin: Alignment.centerLeft,
                end: Alignment.centerRight,
                colors: [
                  Color(0xFF8D6CFF),
                  Color(0xFFD19CFF),
                  Color(0xFF6F8CFF),
                ],
              ).createShader(bounds);
            },
            child: Text(
              isListening
                  ? 'LISTENING...'
                  : 'TAP TO SPEAK',
              style: GoogleFonts.spaceGrotesk(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                letterSpacing: 2.6,
                shadows: const [
                  Shadow(
                    color: Color(0x885F36FF),
                    blurRadius: 14,
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}