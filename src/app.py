from flask import Flask, jsonify, request

app = Flask(__name__)

# Declarar la variable global todos
todos = [
    { "label": "My first task", "done": False }
]

@app.route('/todos', methods=['GET'])
def get_todos():
    # Retornar la versión en JSON de la variable todos
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_new_todo():
    request_body = request.json
    
    # Verificar que el cuerpo de la solicitud sea válido
    if not request_body or not isinstance(request_body, dict):
        return jsonify({"error": "Invalid request body. Should be a JSON object."}), 400
    if "label" not in request_body or "done" not in request_body:
        return jsonify({"error": "Request body must include 'label' and 'done' keys."}), 400
    if not isinstance(request_body["label"], str):
        return jsonify({"error": "The 'label' of the new todo should be a string."}), 400
    if not isinstance(request_body["done"], bool):
        return jsonify({"error": "The 'done' value of the new todo should be a boolean."}), 400

    # Añadir la nueva tarea a la lista todos
    todos.append(request_body)
    
    # Retornar la lista actualizada
    return jsonify(todos)

@app.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
    # Verificar si la posición está dentro de los límites válidos
    if position < 0 or position >= len(todos):
        return jsonify({"error": "Index out of range"}), 404
    
    # Eliminar la tarea en la posición especificada
    deleted_todo = todos.pop(position)
    
    # Retornar la tarea eliminada como respuesta
    return jsonify(deleted_todo)

# Endpoint para eliminar todos los todos (sí, el nombre es intencionalmente redundante)
@app.route('/todos', methods=['DELETE'])
def delete_all_todos():
    global todos
    todos = []  # Vaciar la lista de todos
    return jsonify({"message": "All todos have been deleted."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
