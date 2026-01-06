// src/app/settings/page.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function SettingsPage() {
  const [apiKeys, setApiKeys] = useState([
    { id: '1', name: 'Development Key', value: '...xyz123', createdAt: '2023-01-15' },
    { id: '2', name: 'Production Key', value: '...abc456', createdAt: '2023-02-20' },
  ]);
  const [newKeyName, setNewKeyName] = useState('');

  const handleCreateApiKey = () => {
    if (newKeyName.trim()) {
      // In a real app, this would call an API
      const newKey = {
        id: (apiKeys.length + 1).toString(),
        name: newKeyName,
        value: `...${Math.random().toString(36).substring(2, 8)}`,
        createdAt: new Date().toISOString().split('T')[0],
      };
      setApiKeys([...apiKeys, newKey]);
      setNewKeyName('');
    }
  };

  const handleDeleteApiKey = (id: string) => {
    setApiKeys(apiKeys.filter(key => key.id !== id));
  };

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Settings</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>API Keys</CardTitle>
            <CardDescription>Manage your API keys for accessing Mimicus services</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input
                placeholder="New key name"
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
              />
              <Button onClick={handleCreateApiKey}>Create</Button>
            </div>

            <div className="space-y-2">
              {apiKeys.map((key) => (
                <div key={key.id} className="flex justify-between items-center p-3 border rounded">
                  <div>
                    <div className="font-medium">{key.name}</div>
                    <div className="text-sm text-muted-foreground">{key.value} • Created: {key.createdAt}</div>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Rotate</Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      onClick={() => handleDeleteApiKey(key.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      Delete
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>System Configuration</CardTitle>
            <CardDescription>Configure global settings for your Mimicus instance</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">Backend API URL</label>
              <Input defaultValue="http://localhost:8000" />
            </div>
            
            <div>
              <label className="text-sm font-medium">Logging Level</label>
              <select className="w-full p-2 border rounded mt-1">
                <option>Info</option>
                <option>Debug</option>
                <option>Warning</option>
                <option>Error</option>
              </select>
            </div>
            
            <div>
              <label className="text-sm font-medium">Max Request Logs</label>
              <Input type="number" defaultValue="10000" />
            </div>
            
            <Button className="w-full">Save Configuration</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Import/Export</CardTitle>
            <CardDescription>Backup and restore your mock configurations</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col gap-2">
              <Button variant="outline">
                Export All Mocks
              </Button>
              <Button variant="outline">
                Import Mocks
              </Button>
              <Button variant="outline">
                Export State
              </Button>
              <Button variant="outline">
                Import State
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>About Mimicus</CardTitle>
            <CardDescription>Information about your Mimicus instance</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Version</span>
                <span>v1.0.0</span>
              </div>
              <div className="flex justify-between">
                <span>Database</span>
                <Badge variant="outline">SQLite</Badge>
              </div>
              <div className="flex justify-between">
                <span>Storage</span>
                <Badge variant="outline">Local</Badge>
              </div>
              <div className="flex justify-between">
                <span>Uptime</span>
                <span>24 days</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}