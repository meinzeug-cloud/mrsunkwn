import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { useAPI } from '../hooks/useAPI';
import { useAuth } from '../hooks/useAuth';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { useMrsUnkwnFeatures } from '../hooks/useMrsUnkwnFeatures';

// Mrs-Unkwn specific interfaces
interface GamificationDashboardProps {
  userId?: string;
  familyId?: string;
  studentId?: string;
  parentMode?: boolean;
  className?: string;
  theme?: 'light' | 'dark' | 'student' | 'parent';
  learningMode?: 'socratic' | 'guided' | 'practice' | 'assessment';
  subjectAreas?: string[];
  difficultyLevel?: number;
  aiInteractionEnabled?: boolean;
  monitoringLevel?: 'minimal' | 'standard' | 'strict';
  gamificationEnabled?: boolean;
  parentalControlsActive?: boolean;
  realTimeUpdates?: boolean;
  onLearningEvent?: (event: LearningEvent) => void;
  onSafetyAlert?: (alert: SafetyAlert) => void;
  onParentIntervention?: (intervention: ParentIntervention) => void;
}

interface LearningEvent {
  type: 'start' | 'pause' | 'complete' | 'ai_interaction' | 'achievement';
  data: any;
  timestamp: Date;
  userId: string;
}

interface SafetyAlert {
  level: 'low' | 'medium' | 'high' | 'critical';
  type: 'inappropriate_content' | 'cheating_attempt' | 'external_ai_usage' | 'time_violation';
  description: string;
  evidence?: any;
  recommendedAction: string;
  timestamp: Date;
}

interface ParentIntervention {
  action: 'pause' | 'resume' | 'block' | 'redirect' | 'message';
  reason: string;
  parentId: string;
  timestamp: Date;
}

// Main Mrs-Unkwn Component
export const GamificationDashboard: React.FC<GamificationDashboardProps> = ({
  userId,
  familyId,
  studentId,
  parentMode = false,
  className = '',
  theme = 'student',
  learningMode = 'socratic',
  subjectAreas = [],
  difficultyLevel = 5,
  aiInteractionEnabled = true,
  monitoringLevel = 'standard',
  gamificationEnabled = true,
  parentalControlsActive = true,
  realTimeUpdates = true,
  onLearningEvent,
  onSafetyAlert,
  onParentIntervention
}) => {
  // State management for Mrs-Unkwn features
  const [learningState, setLearningState] = useState({
    isActive: false,
    currentSubject: subjectAreas[0] || '',
    sessionDuration: 0,
    aiInteractions: 0,
    achievements: [],
    currentStreak: 0,
    safetyScore: 100,
    interventionsPending: 0
  });

  const [monitoringData, setMonitoringData] = useState({
    deviceStatus: 'secure',
    browserActivity: [],
    suspiciousEvents: [],
    parentalOverrides: [],
    lastSafetyCheck: new Date()
  });

  const [aiTutorState, setAiTutorState] = useState({
    isInitialized: false,
    personality: 'encouraging',
    currentContext: null,
    conversationHistory: [],
    confidence: 0.8
  });

  // Refs for real-time updates
  const webSocketRef = useRef<WebSocket | null>(null);
  const learningTimerRef = useRef<NodeJS.Timeout | null>(null);
  const monitoringIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Custom hooks for Mrs-Unkwn features
  const { user, isAuthenticated } = useAuth();
  const {
    startLearningSession,
    pauseLearningSession,
    endLearningSession,
    sendAIMessage,
    reportSafetyEvent,
    applyParentIntervention
  } = useMrsUnkwnFeatures();

  // Local storage for preferences
  const [preferences, setPreferences] = useLocalStorage(`gamificationdashboard_preferences`, {
    theme: 'student',
    difficultyLevel: 5,
    preferredSubjects: [],
    aiPersonality: 'encouraging',
    notificationSettings: {
      learningReminders: true,
      achievementAlerts: true,
      safetyAlerts: true
    }
  });

  // API endpoints for Mrs-Unkwn specific data
  const learningSessionAPI = useMemo(() => {
    const baseUrl = userId 
      ? `/api/learning-sessions/user/${userId}`
      : '/api/learning-sessions';
    
    const params = new URLSearchParams();
    if (familyId) params.append('family_id', familyId);
    if (studentId) params.append('student_id', studentId);
    if (subjectAreas.length > 0) params.append('subjects', subjectAreas.join(','));
    
    return `${baseUrl}?${params.toString()}`;
  }, [userId, familyId, studentId, subjectAreas]);

  // Real-time data fetching
  const { data: sessionData, loading, error, refetch } = useAPI(learningSessionAPI, {
    autoRefresh: realTimeUpdates,
    refreshInterval: 5000
  });

  // Initialize Mrs-Unkwn features
  useEffect(() => {
    if (isAuthenticated && userId) {
      initializeMrsUnkwnFeatures();
    }
    
    return () => {
      cleanup();
    };
  }, [isAuthenticated, userId]);

  // Real-time monitoring setup
  useEffect(() => {
    if (realTimeUpdates && monitoringLevel !== 'minimal') {
      setupRealTimeMonitoring();
    }
    
    return () => {
      if (webSocketRef.current) {
        webSocketRef.current.close();
      }
    };
  }, [realTimeUpdates, monitoringLevel]);

  // Learning session timer
  useEffect(() => {
    if (learningState.isActive) {
      learningTimerRef.current = setInterval(() => {
        setLearningState(prev => ({
          ...prev,
          sessionDuration: prev.sessionDuration + 1
        }));
      }, 1000);
    } else {
      if (learningTimerRef.current) {
        clearInterval(learningTimerRef.current);
      }
    }
    
    return () => {
      if (learningTimerRef.current) {
        clearInterval(learningTimerRef.current);
      }
    };
  }, [learningState.isActive]);

  // Initialize Mrs-Unkwn features
  const initializeMrsUnkwnFeatures = async () => {
    try {
      // Initialize AI tutor
      if (aiInteractionEnabled) {
        const aiResponse = await fetch('/api/ai-tutor/initialize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId,
            learningMode,
            subjectAreas,
            difficultyLevel
          })
        });
        
        const aiData = await aiResponse.json();
        setAiTutorState(prev => ({
          ...prev,
          isInitialized: true,
          personality: aiData.personality || 'encouraging',
          currentContext: aiData.context
        }));
      }

      // Initialize monitoring if enabled
      if (parentalControlsActive && monitoringLevel !== 'minimal') {
        await initializeDeviceMonitoring();
      }

      console.log('Mrs-Unkwn features initialized successfully');
    } catch (error) {
      console.error('Failed to initialize Mrs-Unkwn features:', error);
    }
  };

  // Setup real-time monitoring
  const setupRealTimeMonitoring = () => {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/monitoring/${userId}`;
    
    webSocketRef.current = new WebSocket(wsUrl);
    
    webSocketRef.current.onopen = () => {
      console.log('Mrs-Unkwn real-time monitoring connected');
    };
    
    webSocketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleRealTimeUpdate(data);
    };
    
    webSocketRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    webSocketRef.current.onclose = () => {
      console.log('Mrs-Unkwn monitoring disconnected');
      // Attempt to reconnect after 5 seconds
      setTimeout(setupRealTimeMonitoring, 5000);
    };
  };

  // Handle real-time updates
  const handleRealTimeUpdate = useCallback((data: any) => {
    switch (data.type) {
      case 'safety_alert':
        handleSafetyAlert(data.payload);
        break;
      case 'parent_intervention':
        handleParentIntervention(data.payload);
        break;
      case 'learning_event':
        handleLearningEvent(data.payload);
        break;
      case 'monitoring_update':
        updateMonitoringData(data.payload);
        break;
      default:
        console.log('Unknown real-time update:', data);
    }
  }, []);

  // Handle safety alerts
  const handleSafetyAlert = useCallback((alert: SafetyAlert) => {
    setMonitoringData(prev => ({
      ...prev,
      suspiciousEvents: [...prev.suspiciousEvents, alert],
      lastSafetyCheck: new Date()
    }));
    
    // Update safety score
    const scoreDeduction = {
      'low': 5,
      'medium': 15,
      'high': 30,
      'critical': 50
    }[alert.level] || 10;
    
    setLearningState(prev => ({
      ...prev,
      safetyScore: Math.max(0, prev.safetyScore - scoreDeduction)
    }));
    
    // Trigger callback
    onSafetyAlert?.(alert);
    
    // Auto-pause for critical alerts
    if (alert.level === 'critical') {
      pauseLearning('Critical safety alert detected');
    }
  }, [onSafetyAlert]);

  // Handle parent interventions
  const handleParentIntervention = useCallback((intervention: ParentIntervention) => {
    switch (intervention.action) {
      case 'pause':
        pauseLearning('Parent intervention: paused');
        break;
      case 'resume':
        resumeLearning();
        break;
      case 'block':
        blockCurrentActivity(intervention.reason);
        break;
      case 'redirect':
        redirectToSafeActivity();
        break;
      case 'message':
        showParentMessage(intervention.reason);
        break;
    }
    
    setLearningState(prev => ({
      ...prev,
      interventionsPending: prev.interventionsPending + 1
    }));
    
    onParentIntervention?.(intervention);
  }, [onParentIntervention]);

  // Learning session controls
  const startLearning = useCallback(async (subject: string) => {
    try {
      const session = await startLearningSession({
        userId,
        familyId,
        subject,
        learningMode,
        difficultyLevel,
        aiInteractionEnabled
      });
      
      setLearningState(prev => ({
        ...prev,
        isActive: true,
        currentSubject: subject,
        sessionDuration: 0
      }));
      
      const event: LearningEvent = {
        type: 'start',
        data: { subject, sessionId: session.id },
        timestamp: new Date(),
        userId: userId || ''
      };
      
      onLearningEvent?.(event);
      
    } catch (error) {
      console.error('Failed to start learning session:', error);
    }
  }, [userId, familyId, learningMode, difficultyLevel, aiInteractionEnabled, onLearningEvent]);

  const pauseLearning = useCallback(async (reason: string = 'User paused') => {
    try {
      await pauseLearningSession(reason);
      
      setLearningState(prev => ({
        ...prev,
        isActive: false
      }));
      
      const event: LearningEvent = {
        type: 'pause',
        data: { reason },
        timestamp: new Date(),
        userId: userId || ''
      };
      
      onLearningEvent?.(event);
      
    } catch (error) {
      console.error('Failed to pause learning session:', error);
    }
  }, [userId, onLearningEvent]);

  const resumeLearning = useCallback(() => {
    setLearningState(prev => ({
      ...prev,
      isActive: true
    }));
  }, []);

  // AI Tutor interactions
  const sendMessageToAI = useCallback(async (message: string) => {
    if (!aiTutorState.isInitialized || !aiInteractionEnabled) {
      return;
    }
    
    try {
      const response = await sendAIMessage({
        message,
        context: aiTutorState.currentContext,
        learningMode,
        difficultyLevel
      });
      
      setAiTutorState(prev => ({
        ...prev,
        conversationHistory: [...prev.conversationHistory, {
          user: message,
          ai: response.message,
          timestamp: new Date()
        }],
        confidence: response.confidence || prev.confidence
      }));
      
      setLearningState(prev => ({
        ...prev,
        aiInteractions: prev.aiInteractions + 1
      }));
      
      const event: LearningEvent = {
        type: 'ai_interaction',
        data: { message, response },
        timestamp: new Date(),
        userId: userId || ''
      };
      
      onLearningEvent?.(event);
      
      return response;
      
    } catch (error) {
      console.error('AI interaction failed:', error);
      return { error: 'AI tutor is temporarily unavailable' };
    }
  }, [aiTutorState, aiInteractionEnabled, learningMode, difficultyLevel, userId, onLearningEvent]);

  // Render component sections
  const renderLearningInterface = () => (
    <div className="learning-interface">
      <div className="learning-header">
        <h2>Mrs-Unkwn Learning Session</h2>
        <div className="session-info">
          <span>Subject: {learningState.currentSubject}</span>
          <span>Duration: {Math.floor(learningState.sessionDuration / 60)}:{String(learningState.sessionDuration % 60).padStart(2, '0')}</span>
          <span className={`safety-score ${learningState.safetyScore < 50 ? 'low' : ''}`}>
            Safety: {learningState.safetyScore}%
          </span>
        </div>
      </div>
      
      {aiInteractionEnabled && aiTutorState.isInitialized && (
        <div className="ai-tutor-section">
          <h3>🤖 Your AI Tutor (Mrs-Unkwn)</h3>
          <div className="conversation-history">
            {aiTutorState.conversationHistory.map((item, index) => (
              <div key={index} className="conversation-item">
                <div className="user-message">You: {item.user}</div>
                <div className="ai-message">Mrs-Unkwn: {item.ai}</div>
              </div>
            ))}
          </div>
          <div className="ai-input">
            <input
              type="text"
              placeholder="Ask Mrs-Unkwn for help..."
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  sendMessageToAI(e.currentTarget.value);
                  e.currentTarget.value = '';
                }
              }}
            />
          </div>
        </div>
      )}
    </div>
  );

  const renderParentControls = () => parentMode && (
    <div className="parent-controls">
      <h3>👨‍👩‍👧‍👦 Parent Controls</h3>
      <div className="control-buttons">
        <button onClick={() => pauseLearning('Parent pause')}>
          ⏸️ Pause Session
        </button>
        <button onClick={resumeLearning}>
          ▶️ Resume Session  
        </button>
        <button onClick={() => handleParentIntervention({
          action: 'block',
          reason: 'Parent block',
          parentId: userId || '',
          timestamp: new Date()
        })}>
          🚫 Block Current Activity
        </button>
      </div>
      
      <div className="monitoring-status">
        <h4>Monitoring Status</h4>
        <p>Device: {monitoringData.deviceStatus}</p>
        <p>Suspicious Events: {monitoringData.suspiciousEvents.length}</p>
        <p>Last Check: {monitoringData.lastSafetyCheck.toLocaleTimeString()}</p>
      </div>
    </div>
  );

  const renderGamification = () => gamificationEnabled && (
    <div className="gamification-section">
      <h3>🎮 Your Progress</h3>
      <div className="achievements">
        <span>🏆 Achievements: {learningState.achievements.length}</span>
        <span>🔥 Streak: {learningState.currentStreak} days</span>
        <span>💬 AI Chats: {learningState.aiInteractions}</span>
      </div>
    </div>
  );

  // Helper functions
  const initializeDeviceMonitoring = async () => {
    // Implementation for device monitoring initialization
  };

  const updateMonitoringData = (data: any) => {
    setMonitoringData(prev => ({ ...prev, ...data }));
  };

  const blockCurrentActivity = (reason: string) => {
    console.log('Blocking current activity:', reason);
  };

  const redirectToSafeActivity = () => {
    console.log('Redirecting to safe activity');
  };

  const showParentMessage = (message: string) => {
    alert(`Message from parent: ${message}`);
  };

  const cleanup = () => {
    if (learningTimerRef.current) clearInterval(learningTimerRef.current);
    if (monitoringIntervalRef.current) clearInterval(monitoringIntervalRef.current);
    if (webSocketRef.current) webSocketRef.current.close();
  };

  // Main render
  return (
    <div className={`mrs-unkwn-gamificationdashboard theme-${theme} ${className}`}>
      <div className="component-header">
        <h1>Mrs-Unkwn - GamificationDashboard</h1>
        {parentMode && <span className="parent-mode-indicator">👨‍👩‍👧‍👦 Parent Mode</span>}
      </div>

      {loading && (
        <div className="loading-state">
          <div className="loading-spinner">Loading Mrs-Unkwn...</div>
        </div>
      )}

      {error && (
        <div className="error-state">
          <h3>Mrs-Unkwn Error</h3>
          <p>{error.message}</p>
          <button onClick={refetch}>Try Again</button>
        </div>
      )}

      {!loading && !error && (
        <div className="component-content">
          {renderLearningInterface()}
          {renderParentControls()}
          {renderGamification()}
          
          <div className="mrs-unkwn-footer">
            <p>Mrs-Unkwn - Your intelligent, safe learning companion 🤖📚</p>
            <p>Always learning together, never cheating alone!</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default GamificationDashboard;
