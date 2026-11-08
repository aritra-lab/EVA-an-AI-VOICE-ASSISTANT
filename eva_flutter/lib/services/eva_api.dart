import 'dart:convert';

import 'package:http/http.dart' as http;

class EvaApi {
  static const String baseUrl =
      'http://127.0.0.1:5000';

  static Future<String> sendMessage(
    String message,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'message': message,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception(
        'EVA API error: ${response.statusCode}',
      );
    }

    final data = jsonDecode(
      response.body,
    );

    return data['reply']?.toString() ??
        'EVA did not return a response.';
  }

  static Future<String> listen() async {
    final response = await http.post(
      Uri.parse('$baseUrl/listen'),
    );

    if (response.statusCode != 200) {
      throw Exception(
        'EVA speech API error: ${response.statusCode}',
      );
    }

    final data = jsonDecode(
      response.body,
    );

    return data['command']?.toString() ?? '';
  }

  static Future<Map<String, dynamic>>
      getStartupInfo() async {
    final response = await http.get(
      Uri.parse('$baseUrl/startup'),
    );

    if (response.statusCode != 200) {
      throw Exception(
        'EVA startup API error: ${response.statusCode}',
      );
    }

    final data = jsonDecode(
      response.body,
    );

    return Map<String, dynamic>.from(data);
  }

  static Future<void> speak(
    String message,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/speak'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'message': message,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception(
        'EVA speak API error: ${response.statusCode}',
      );
    }
  }
}