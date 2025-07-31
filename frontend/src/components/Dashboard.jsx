import { useState, useEffect } from 'react'
import { 
  Shield, 
  AlertTriangle, 
  Server, 
  Users, 
  TrendingUp, 
  TrendingDown,
  Activity,
  Eye,
  Lock,
  Zap
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'

const Dashboard = () => {
  const [securityScore, setSecurityScore] = useState(85)
  const [loading, setLoading] = useState(true)

  // Sample data for charts
  const incidentTrends = [
    { date: '2024-01-01', incidents: 12, resolved: 10 },
    { date: '2024-01-02', incidents: 8, resolved: 8 },
    { date: '2024-01-03', incidents: 15, resolved: 12 },
    { date: '2024-01-04', incidents: 6, resolved: 6 },
    { date: '2024-01-05', incidents: 9, resolved: 7 },
    { date: '2024-01-06', incidents: 11, resolved: 11 },
    { date: '2024-01-07', incidents: 4, resolved: 4 },
  ]

  const threatTypes = [
    { name: 'Malware', value: 35, color: '#ef4444' },
    { name: 'Phishing', value: 28, color: '#f97316' },
    { name: 'DDoS', value: 20, color: '#eab308' },
    { name: 'Data Breach', value: 17, color: '#22c55e' },
  ]

  const assetHealth = [
    { category: 'Servers', healthy: 85, warning: 12, critical: 3 },
    { category: 'Workstations', healthy: 92, warning: 6, critical: 2 },
    { category: 'Network Devices', healthy: 78, warning: 18, critical: 4 },
    { category: 'Applications', healthy: 88, warning: 10, critical: 2 },
  ]

  const recentIncidents = [
    {
      id: 1,
      title: 'Suspicious Login Attempt',
      severity: 'high',
      status: 'investigating',
      time: '2 minutes ago',
      asset: 'Web Server 01'
    },
    {
      id: 2,
      title: 'Malware Detection',
      severity: 'critical',
      status: 'contained',
      time: '15 minutes ago',
      asset: 'Workstation 45'
    },
    {
      id: 3,
      title: 'Unauthorized Access',
      severity: 'medium',
      status: 'resolved',
      time: '1 hour ago',
      asset: 'Database Server'
    },
    {
      id: 4,
      title: 'Network Anomaly',
      severity: 'low',
      status: 'monitoring',
      time: '3 hours ago',
      asset: 'Router 02'
    }
  ]

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500'
      case 'high': return 'bg-orange-500'
      case 'medium': return 'bg-yellow-500'
      case 'low': return 'bg-green-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'resolved': return 'text-green-600 bg-green-100'
      case 'investigating': return 'text-orange-600 bg-orange-100'
      case 'contained': return 'text-blue-600 bg-blue-100'
      case 'monitoring': return 'text-purple-600 bg-purple-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => setLoading(false), 1000)
    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Security Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400">Real-time cybersecurity monitoring and analytics</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-green-600 border-green-600">
            <Activity className="w-3 h-3 mr-1" />
            System Healthy
          </Badge>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Security Score</CardTitle>
            <Shield className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{securityScore}%</div>
            <div className="flex items-center space-x-2 mt-2">
              <Progress value={securityScore} className="flex-1" />
              <TrendingUp className="h-4 w-4 text-green-500" />
            </div>
            <p className="text-xs text-muted-foreground mt-1">+2% from last week</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Threats</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">7</div>
            <div className="flex items-center space-x-1 mt-2">
              <TrendingDown className="h-4 w-4 text-green-500" />
              <span className="text-xs text-green-600">-3 from yesterday</span>
            </div>
            <p className="text-xs text-muted-foreground">2 critical, 3 high, 2 medium</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Protected Assets</CardTitle>
            <Server className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">1,247</div>
            <div className="flex items-center space-x-1 mt-2">
              <TrendingUp className="h-4 w-4 text-green-500" />
              <span className="text-xs text-green-600">+12 new assets</span>
            </div>
            <p className="text-xs text-muted-foreground">98.5% coverage</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Users</CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">342</div>
            <div className="flex items-center space-x-1 mt-2">
              <Activity className="h-4 w-4 text-blue-500" />
              <span className="text-xs text-blue-600">89 online now</span>
            </div>
            <p className="text-xs text-muted-foreground">26% increase this month</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Incident Trends */}
        <Card>
          <CardHeader>
            <CardTitle>Incident Trends</CardTitle>
            <CardDescription>Daily incident reports and resolution rates</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={incidentTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <YAxis />
                <Tooltip 
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <Area 
                  type="monotone" 
                  dataKey="incidents" 
                  stackId="1"
                  stroke="#ef4444" 
                  fill="#ef4444" 
                  fillOpacity={0.6}
                  name="New Incidents"
                />
                <Area 
                  type="monotone" 
                  dataKey="resolved" 
                  stackId="2"
                  stroke="#22c55e" 
                  fill="#22c55e" 
                  fillOpacity={0.6}
                  name="Resolved"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Threat Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Threat Distribution</CardTitle>
            <CardDescription>Current threat landscape breakdown</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={threatTypes}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {threatTypes.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${value}%`, 'Percentage']} />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-wrap justify-center gap-4 mt-4">
              {threatTypes.map((threat, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: threat.color }}
                  />
                  <span className="text-sm">{threat.name}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Asset Health and Recent Incidents */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Asset Health */}
        <Card>
          <CardHeader>
            <CardTitle>Asset Health Overview</CardTitle>
            <CardDescription>Current status of protected assets</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={assetHealth} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="category" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="healthy" stackId="a" fill="#22c55e" name="Healthy" />
                <Bar dataKey="warning" stackId="a" fill="#eab308" name="Warning" />
                <Bar dataKey="critical" stackId="a" fill="#ef4444" name="Critical" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Recent Incidents */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Incidents</CardTitle>
            <CardDescription>Latest security incidents and their status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentIncidents.map((incident) => (
                <div key={incident.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${getSeverityColor(incident.severity)}`} />
                    <div>
                      <p className="font-medium text-sm">{incident.title}</p>
                      <p className="text-xs text-gray-500">{incident.asset} • {incident.time}</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className={getStatusColor(incident.status)}>
                    {incident.status}
                  </Badge>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              <Eye className="w-4 h-4 mr-2" />
              View All Incidents
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common security operations and tools</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Zap className="w-6 h-6" />
              <span className="text-sm">Run Scan</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Lock className="w-6 h-6" />
              <span className="text-sm">Lock Assets</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <AlertTriangle className="w-6 h-6" />
              <span className="text-sm">Create Incident</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Activity className="w-6 h-6" />
              <span className="text-sm">System Health</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

