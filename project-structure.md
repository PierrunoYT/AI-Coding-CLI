# Project Structure - AI Chat CLI

## 📁 **Directory Tree**

```
AI Coding CLI/
├── 📄 LICENSE                    # MIT License for open source distribution
├── 🎯 main.py                    # Core application and CLI interface (576 lines)
├── 📚 README.md                  # Comprehensive user documentation and setup guide
├── 📦 requirements.txt           # Python dependencies (requests, rich)
├── 📋 tasks.md                   # Complete development history and documentation
├── 🧪 test_api.py               # API connection testing utility
├── 🛠️ tools.py                  # File system tools and function definitions (369 lines)
├── 🤖 CLAUDE.md                 # Development guidance for Claude Code instances
├── 🔍 code-issues.md            # Code quality analysis and issue tracking
└── 📝 project-structure.md      # This file - Project architecture overview
```

## 🏗️ **Architecture Overview**

### **Core Application Layer**
```
📱 User Interface
    ↓
🎯 main.py (CLI Controller)
    ↓
🔌 ChatClient (API Integration)
    ↓
🌐 OpenRouter API
```

### **Tool System Layer**
```
🤖 AI Agent Mode
    ↓
🛠️ tools.py (Function Definitions)
    ↓
💻 File System Operations
```

## 📄 **File Breakdown & Responsibilities**

### **🎯 main.py** - *Core Application* (576 lines)
The heart of the application containing:

#### **Configuration Management**
- `Config` class - Environment variables, model settings, agent mode
- API key validation and format checking
- Debug mode and tool execution configuration

#### **API Client Implementation**
- `ChatClient` class - Complete OpenRouter integration
- HTTP error handling with retry logic
- Model compatibility detection
- Connection testing and validation

#### **User Interface**
- Rich console interface with styled output
- Interactive command processing
- Progress indicators and visual feedback
- Markdown help system rendering

#### **Tool Orchestration**
- Sequential and parallel tool execution
- Tool call limiting and safety measures
- Smart tool promise detection with behavioral analysis
- Result processing and display
- Conversation history management

#### **CLI Commands**
```
/help     - Comprehensive help system
/model    - Current model display
/models   - Interactive model selection
/agent    - Toggle coding agent mode
/parallel - Tool execution mode toggle
/max-tools- Configure tool call limits
/stats    - Usage statistics display
/reset    - Conversation history reset
/clear    - Console screen clearing
/exit     - Application termination
```

### **🛠️ tools.py** - *Tool System* (369 lines)
Comprehensive file system operations:

#### **Directory Operations**
```python
list_files()         # Browse directories with icons
create_directory()   # Recursive directory creation
```

#### **File Reading Operations**
```python
read_file()          # Complete file content reading
read_file_lines()    # Selective line range reading
```

#### **File Writing Operations**
```python
write_to_file()      # File creation/overwriting
append_to_file()     # Content appending
insert_line_at_position() # Precise line insertion
```

#### **File Editing Operations**
```python
replace_in_file()    # Find and replace functionality
```

#### **File Management**
```python
delete_file()        # Safe deletion with confirmation
```

#### **Code Execution**
```python
execute_python_file() # Safe script execution with timeout
```

#### **Function Definitions**
- OpenAI-compatible tool definitions (`TOOLS_DEFINITIONS`)
- Tool mapping and registration (`AVAILABLE_TOOLS`)
- Comprehensive parameter validation
- Safety and error handling for all operations

### **🧪 test_api.py** - *Testing Utility*
Standalone API validation script:
- API key format and presence validation
- OpenRouter connection testing
- Authentication verification
- Model availability checking
- Troubleshooting assistance

### **📚 README.md** - *User Documentation*
Comprehensive user guide including:
- **Setup Instructions**: Platform-specific installation
- **Feature Documentation**: Complete feature overview
- **Command Reference**: All CLI commands explained
- **Troubleshooting Guide**: Common issues and solutions
- **Model Compatibility**: Function calling support matrix
- **Safety Features**: Security measures documentation

### **📋 tasks.md** - *Development Documentation*
Complete development history:
- **Architecture Documentation**: Technical implementation details
- **Feature Timeline**: Phase-by-phase development history
- **Code Statistics**: Metrics and project scope
- **Implementation Details**: Code examples and patterns
- **Future Roadmap**: Enhancement ideas and optimizations

### **📦 requirements.txt** - *Dependencies*
Minimal dependency management:
```
requests  # HTTP client for API communication
rich      # Terminal styling and UI components
```

### **📄 LICENSE** - *Legal*
MIT License for open source distribution

### **📝 project-structure.md** - *Architecture Guide*
This file - Complete project architecture overview

## 🔧 **Component Interactions**

### **Application Flow**
```
1. 🚀 Application Startup
   ├── Environment validation (API key, config)
   ├── API connection testing
   └── UI initialization

2. 💬 Chat Mode
   ├── User input processing
   ├── Model selection and switching
   └── Conversation management

3. 🤖 Agent Mode
   ├── Tool availability detection
   ├── Function calling integration
   ├── Tool execution (sequential/parallel)
   └── Result processing and feedback

4. 🛡️ Safety & Error Handling
   ├── Input validation
   ├── Error recovery and retry logic
   ├── User confirmations for destructive operations
   └── Timeout protection
```

### **Data Flow Architecture**
```
User Input → Command Parser → ChatClient → OpenRouter API
                ↓
            Tool Detection → Tool Executor → File System
                ↓
            Result Processing → UI Renderer → Console Output
```

## 📊 **Codebase Statistics**

### **File Metrics**
| File | Lines | Purpose | Complexity |
|------|-------|---------|------------|
| `main.py` | 576 | Core application | High |
| `tools.py` | 369 | Tool system | Medium |
| `test_api.py` | ~50 | Testing utility | Low |
| `README.md` | ~200 | Documentation | Low |
| `tasks.md` | ~400 | Dev documentation | Low |

### **Feature Distribution**
- **Core Chat**: ~40% of codebase
- **Agent Tools**: ~35% of codebase  
- **Error Handling**: ~15% of codebase
- **UI/UX**: ~10% of codebase

### **Code Organization**
- **Classes**: 2 main classes (`Config`, `ChatClient`)
- **Functions**: 10 file system tools + 8 UI functions
- **Commands**: 11 CLI commands
- **Tools**: 10 agent tools with OpenAI function definitions

## 🎯 **Design Patterns**

### **Configuration Pattern**
- Centralized configuration management
- Environment variable integration
- Validation and default values

### **Client-Server Pattern**
- Clean API abstraction layer
- Error handling and retry logic
- Request/response processing

### **Command Pattern**
- CLI command registration and processing
- Extensible command system
- Context-aware command availability

### **Strategy Pattern**
- Tool execution modes (sequential/parallel)
- Model compatibility handling
- Error recovery strategies

### **Observer Pattern**
- Progress tracking and feedback
- Status updates and notifications
- Real-time execution monitoring

## 🔮 **Extensibility Points**

### **Adding New Tools**
1. Implement function in `tools.py`
2. Add to `TOOLS_DEFINITIONS` array
3. Update `AVAILABLE_TOOLS` mapping
4. Test with agent mode

### **Adding New Commands**
1. Add command handler in `main()` function
2. Update help system documentation
3. Add to README command reference

### **Adding New Models**
1. Update compatibility detection logic
2. Test function calling support
3. Update documentation

### **Adding New Features**
1. Extend `Config` class for settings
2. Implement in `ChatClient` class
3. Add UI components and feedback
4. Update documentation

## 🚀 **Deployment Structure**

### **Development Environment**
```
Local Development/
├── Python 3.7+ runtime
├── Virtual environment (recommended)
├── OpenRouter API key
└── Terminal with Unicode support
```

### **Production Ready**
- ✅ Standalone Python application
- ✅ Minimal dependencies (2 packages)
- ✅ Cross-platform compatibility
- ✅ Environment variable configuration
- ✅ Comprehensive error handling
- ✅ User safety measures

---

**Project Complexity**: Medium  
**Maintainability**: High  
**Extensibility**: High  
**Documentation Coverage**: Complete  
**Test Coverage**: Manual testing + API validation utility 