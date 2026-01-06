// src/app/state/page.tsx
"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { apiClient } from "@/lib/api-client";
import { StateValue } from "@/types/api";

export default function StatePage() {
  const [states, setStates] = useState<StateValue[]>([]);
  const [sessionFilter, setSessionFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStates();
  }, []);

  const fetchStates = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get<StateValue[]>('/api/admin/state');
      setStates(data);
    } catch (error) {
      console.error('Error fetching states:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredStates = sessionFilter 
    ? states.filter(state => state.session_id.includes(sessionFilter))
    : states;

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading state values...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">State Management</h1>
        <Button onClick={fetchStates}>Refresh</Button>
      </div>

      <div className="mb-6">
        <div className="flex gap-2">
          <Input
            placeholder="Filter by session ID..."
            value={sessionFilter}
            onChange={(e) => setSessionFilter(e.target.value)}
          />
          <Button variant="outline">Clear</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredStates.map((state) => (
          <Card key={state.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-lg">{state.key}</CardTitle>
                <Badge variant="outline">{state.session_id.substring(0, 8)}...</Badge>
              </div>
              <CardDescription>
                Updated: {new Date(state.updated_at).toLocaleString()}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <h4 className="font-medium mb-2">Value</h4>
                <pre className="bg-muted p-3 rounded text-sm overflow-x-auto">
                  {state.value}
                </pre>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">Edit</Button>
                <Button variant="outline" size="sm">Delete</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredStates.length === 0 && (
        <Card>
          <CardContent className="py-10 text-center">
            <p className="text-muted-foreground">No state values found</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}