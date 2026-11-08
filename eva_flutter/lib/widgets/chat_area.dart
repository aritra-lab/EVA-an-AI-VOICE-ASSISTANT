import 'dart:math';

import 'package:flutter/material.dart';

import '../services/eva_api.dart';

class EvaChatArea extends StatefulWidget {
  const EvaChatArea({super.key});

  @override
  EvaChatAreaState createState() => EvaChatAreaState();
}

class EvaChatAreaState extends State<EvaChatArea> {
  final TextEditingController messageController =
      TextEditingController();

  final ScrollController scrollController =
      ScrollController();

  final List<Map<String, String>> messages = [];

  bool isSending = false;
  bool isStartupRunning = true;

  @override
  void initState() {
    super.initState();

    _runStartupSequence();
  }

  // ==========================================
  // STARTUP SEQUENCE
  // ==========================================

  Future<void> _runStartupSequence() async {
    try {
      // ------------------------------------------
      // STEP 1: GREETING
      // ------------------------------------------

      final greeting = _getGreeting();

      _addEvaMessage(greeting);

      await EvaApi.speak(greeting);

      // ------------------------------------------
      // STEP 2: LOAD REAL STARTUP DATA
      // ------------------------------------------

      final startupInfo =
          await EvaApi.getStartupInfo();

      // ------------------------------------------
      // STEP 3: BUILD STARTUP REPORT
      // ------------------------------------------

      final startupMessages =
          _buildStartupMessages(startupInfo);

      // ------------------------------------------
      // STEP 4: SHOW + SPEAK ONE BY ONE
      // ------------------------------------------

      for (final message in startupMessages) {
        if (!mounted) {
          return;
        }

        _addEvaMessage(message);

        await EvaApi.speak(message);
      }
    } catch (e) {
      if (mounted) {
        _addEvaMessage(
          'EVA startup sequence could not be completed.',
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          isStartupRunning = false;
        });
      }
    }

    scrollToBottom();
  }

  // ==========================================
  // GREETING
  // ==========================================

  String _getGreeting() {
    final hour = DateTime.now().hour;

    String greeting;

    if (hour >= 5 && hour < 12) {
      greeting = 'Good Morning';
    } else if (hour >= 12 && hour < 18) {
      greeting = 'Good Afternoon';
    } else {
      greeting = 'Good Evening';
    }

    final responses = [
      '$greeting Everyone! MYSELF EVA, YOUR PERSONAL ASSISTANT. HOW MAY I HELP YOU MASTER?',
      '$greeting! I AM EVA, YOUR PERSONAL ASSISTANT. WHAT CAN I DO FOR YOU TODAY?',
      '$greeting! I AM EVA, YOUR PERSONAL ASSISTANT. HOW CAN I ASSIST YOU TODAY?',
    ];

    final random = Random();

    return responses[
      random.nextInt(responses.length)
    ];
  }

  // ==========================================
  // STARTUP REPORT BUILDER
  // ==========================================

  List<String> _buildStartupMessages(
    Map<String, dynamic> data,
  ) {
    final int noteCount =
        _toInt(data['note_count']);

    final int totalTasks =
        _toInt(data['total_tasks']);

    final int pendingTasks =
        _toInt(data['pending_tasks']);

    final int dueTasks =
        _toInt(data['due_tasks']);

    final int overdueTasks =
        _toInt(data['overdue_tasks']);

    final List<String> startupMessages = [];

    // ------------------------------------------
    // TASK REMINDERS
    // ------------------------------------------

    if (dueTasks > 0) {
      startupMessages.add(
        'MASTER, YOU HAVE $dueTasks TASKS DUE TODAY.....',
      );
    }

    if (overdueTasks > 0) {
      startupMessages.add(
        'WARNING...!! YOU HAVE $overdueTasks OVER-DUE TASKS.....',
      );
    }

    // ------------------------------------------
    // STARTUP STATISTICS
    // ------------------------------------------

    if (noteCount > 0) {
      startupMessages.add(
        'MASTER, YOU HAVE $noteCount NOTES SAVED',
      );
    }

    if (totalTasks > 0) {
      startupMessages.add(
        'MASTER, YOU HAVE $totalTasks TOTAL TASKS',
      );
    }

    if (pendingTasks > 0) {
      startupMessages.add(
        'MASTER, YOU HAVE $pendingTasks PENDING TASKS',
      );
    }

    // ------------------------------------------
    // NOTHING SAVED
    // ------------------------------------------

    if (noteCount == 0 &&
        totalTasks == 0 &&
        pendingTasks == 0) {
      startupMessages.add(
        'MASTER, YOU HAVE NO NOTES OR TASKS SAVED',
      );
    }

    return startupMessages;
  }

  // ==========================================
  // SAFE INTEGER CONVERSION
  // ==========================================

  int _toInt(dynamic value) {
    if (value is int) {
      return value;
    }

    return int.tryParse(
          value?.toString() ?? '',
        ) ??
        0;
  }

  // ==========================================
  // ADD EVA MESSAGE
  // ==========================================

  void _addEvaMessage(String message) {
    if (!mounted) {
      return;
    }

    setState(() {
      messages.add({
        'role': 'eva',
        'message': message,
      });
    });

    scrollToBottom();
  }

  // ==========================================
  // SEND MESSAGE
  // ==========================================

  Future<void> sendMessage([
    String? voiceMessage,
  ]) async {
    if (isStartupRunning) {
      return;
    }

    final message =
        (voiceMessage ?? messageController.text)
            .trim();

    if (message.isEmpty || isSending) {
      return;
    }

    setState(() {
      messages.add({
        'role': 'user',
        'message': message,
      });

      isSending = true;
      messageController.clear();
    });

    scrollToBottom();

    try {
      final reply = await EvaApi.sendMessage(
        message,
      );

      if (mounted) {
        setState(() {
          messages.add({
            'role': 'eva',
            'message': reply,
          });
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          messages.add({
            'role': 'eva',
            'message':
                'I cannot reach the EVA server. Please make sure the API server is running.',
          });
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          isSending = false;
        });
      }

      scrollToBottom();
    }
  }

  // ==========================================
  // SCROLL TO BOTTOM
  // ==========================================

  void scrollToBottom() {
    WidgetsBinding.instance
        .addPostFrameCallback((_) {
      if (!scrollController.hasClients) {
        return;
      }

      scrollController.animateTo(
        scrollController.position.maxScrollExtent,
        duration: const Duration(
          milliseconds: 300,
        ),
        curve: Curves.easeOut,
      );
    });
  }

  // ==========================================
  // DISPOSE
  // ==========================================

  @override
  void dispose() {
    messageController.dispose();
    scrollController.dispose();
    super.dispose();
  }

  // ==========================================
  // UI
  // ==========================================

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(
        45,
        52,
        45,
        25,
      ),
      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,
        children: [
          Expanded(
            child: messages.isEmpty
                ? const Center(
                    child: Text(
                      'Start a conversation with EVA',
                      style: TextStyle(
                        color: Color(0xFF555A7A),
                        fontSize: 16,
                      ),
                    ),
                  )
                : ListView.builder(
                    controller: scrollController,
                    itemCount: messages.length,
                    itemBuilder:
                        (context, index) {
                      final item =
                          messages[index];

                      final isUser =
                          item['role'] ==
                              'user';

                      return Align(
                        alignment: isUser
                            ? Alignment.centerRight
                            : Alignment.centerLeft,
                        child: Container(
                          constraints:
                              const BoxConstraints(
                            maxWidth: 520,
                          ),
                          margin:
                              const EdgeInsets.only(
                            bottom: 14,
                          ),
                          padding:
                              const EdgeInsets
                                  .symmetric(
                            horizontal: 20,
                            vertical: 16,
                          ),
                          decoration:
                              BoxDecoration(
                            color: isUser
                                ? const Color(
                                    0xFF21194A,
                                  )
                                : const Color(
                                    0xFF10152E,
                                  ),
                            borderRadius:
                                BorderRadius
                                    .circular(
                              18,
                            ),
                            border:
                                Border.all(
                              color: isUser
                                  ? const Color(
                                      0xFF4A397D,
                                    )
                                  : const Color(
                                      0xFF282E57,
                                    ),
                            ),
                          ),
                          child: Text(
                            item['message'] ??
                                '',
                            style:
                                const TextStyle(
                              color:
                                  Colors.white,
                              fontSize: 17,
                              height: 1.5,
                            ),
                          ),
                        ),
                      );
                    },
                  ),
          ),

          const SizedBox(height: 15),

          // ==========================================
          // MESSAGE INPUT
          // ==========================================

          Container(
            height: 62,
            decoration: BoxDecoration(
              color: const Color(
                0xFF0D1229,
              ),
              borderRadius:
                  BorderRadius.circular(18),
              border: Border.all(
                color: const Color(
                  0xFF282E57,
                ),
              ),
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    enabled: !isStartupRunning,
                    controller:
                        messageController,
                    onSubmitted: (_) =>
                        sendMessage(),
                    style:
                        const TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                    ),
                    decoration:
                        const InputDecoration(
                      hintText:
                          'Talk to EVA...',
                      hintStyle:
                          TextStyle(
                        color:
                            Color(0xFF666B8A),
                      ),
                      border:
                          InputBorder.none,
                      contentPadding:
                          EdgeInsets.symmetric(
                        horizontal: 20,
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding:
                      const EdgeInsets.only(
                    right: 8,
                  ),
                  child: IconButton(
                    onPressed:
                        isStartupRunning ||
                                isSending
                            ? null
                            : sendMessage,
                    icon: Icon(
                      Icons
                          .arrow_upward_rounded,
                      color:
                          isStartupRunning ||
                                  isSending
                              ? const Color(
                                  0xFF555A7A,
                                )
                              : const Color(
                                  0xFFB66CFF,
                                ),
                      size: 27,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}