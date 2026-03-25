"use client";

import React, { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

type Severity = "Red" | "Yellow" | "Green";

interface Patient {
  id: string;
  name: string;
  age: number;
  condition: string;
  severity: Severity;
  waitTime: string;
  status: string;
}

const mockPatients: Patient[] = [
  { id: "P-1001", name: "John Doe", age: 45, condition: "Cardiac Arrest", severity: "Red", waitTime: "0 mins", status: "Being Treated" },
  { id: "P-1002", name: "Jane Smith", age: 34, condition: "Severe Asthma", severity: "Red", waitTime: "2 mins", status: "Waiting for Doctor" },
  { id: "P-1003", name: "Robert Johnson", age: 62, condition: "Ankle Sprain", severity: "Green", waitTime: "45 mins", status: "In Triage" },
  { id: "P-1004", name: "Emily Brown", age: 28, condition: "High Fever", severity: "Yellow", waitTime: "15 mins", status: "In Triage" },
  { id: "P-1005", name: "Michael Davis", age: 50, condition: "Chest Pain", severity: "Red", waitTime: "1 min", status: "Being Treated" },
  { id: "P-1006", name: "Sarah Wilson", age: 19, condition: "Minor Cut", severity: "Green", waitTime: "60 mins", status: "Waiting for Doctor" },
  { id: "P-1007", name: "David Miller", age: 71, condition: "Shortness of Breath", severity: "Yellow", waitTime: "10 mins", status: "In Triage" },
];

export default function DoctorDashboard() {
  const [severityFilter, setSeverityFilter] = useState<Severity | "All">("All");

  const filteredPatients = mockPatients.filter(patient => 
    severityFilter === "All" ? true : patient.severity === severityFilter
  );

  const getSeverityColor = (severity: Severity) => {
    switch (severity) {
      case "Red": return "destructive";
      case "Yellow": return "default"; // Will customize with Tailwind
      case "Green": return "secondary";
      default: return "default";
    }
  };

  return (
    <div className="container mx-auto py-10">
      <Card className="shadow-lg border-t-4 border-t-red-500">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle className="text-3xl font-bold tracking-tight text-gray-900">Emergency Room Priority Dashboard</CardTitle>
              <CardDescription className="text-lg mt-2 font-medium">
                Live feed of patient triage status. Prioritize 'Red' severity cases immediately.
              </CardDescription>
            </div>
            <div className="flex items-center space-x-4 bg-gray-50 p-3 rounded-lg border">
              <span className="text-sm font-semibold text-gray-700">Filter by Severity:</span>
              <Select 
                value={severityFilter} 
                onValueChange={(value) => setSeverityFilter(value as Severity | "All")}
              >
                <SelectTrigger className="w-[180px] bg-white font-medium shadow-sm">
                  <SelectValue placeholder="All Severities" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="All">All Patients</SelectItem>
                  <SelectItem value="Red" className="text-red-600 font-bold focus:text-red-700">Red (Critical)</SelectItem>
                  <SelectItem value="Yellow" className="text-yellow-600 font-bold focus:text-yellow-700">Yellow (Urgent)</SelectItem>
                  <SelectItem value="Green" className="text-green-600 font-bold focus:text-green-700">Green (Non-Urgent)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border bg-white shadow-sm overflow-hidden">
            <Table>
              <TableHeader className="bg-gray-100">
                <TableRow>
                  <TableHead className="font-bold text-gray-700">Patient ID</TableHead>
                  <TableHead className="font-bold text-gray-700">Name</TableHead>
                  <TableHead className="font-bold text-gray-700">Age</TableHead>
                  <TableHead className="font-bold text-gray-700">Condition</TableHead>
                  <TableHead className="font-bold text-gray-700">Severity</TableHead>
                  <TableHead className="font-bold text-gray-700">Wait Time</TableHead>
                  <TableHead className="font-bold text-gray-700">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPatients.length > 0 ? (
                  filteredPatients.map((patient) => (
                    <TableRow key={patient.id} className="hover:bg-gray-50 transition-colors">
                      <TableCell className="font-medium text-gray-900">{patient.id}</TableCell>
                      <TableCell className="font-semibold">{patient.name}</TableCell>
                      <TableCell>{patient.age}</TableCell>
                      <TableCell>{patient.condition}</TableCell>
                      <TableCell>
                        {patient.severity === "Red" ? (
                          <Badge variant="destructive" className="animate-pulse shadow-sm px-3 py-1 font-bold text-sm tracking-wide">
                            CRITICAL - {patient.severity}
                          </Badge>
                        ) : patient.severity === "Yellow" ? (
                          <Badge className="bg-yellow-500 hover:bg-yellow-600 shadow-sm px-3 py-1 font-bold text-sm text-yellow-950">
                            URGENT - {patient.severity}
                          </Badge>
                        ) : (
                          <Badge className="bg-green-500 hover:bg-green-600 shadow-sm px-3 py-1 font-bold text-sm">
                            STANDARD - {patient.severity}
                          </Badge>
                        )}
                      </TableCell>
                      <TableCell>
                        <span className={`font-mono font-medium ${patient.severity === 'Red' ? 'text-red-600 font-bold' : ''}`}>
                          {patient.waitTime}
                        </span>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className={`${patient.status === 'Being Treated' ? 'border-primary text-primary bg-primary/10' : 'text-gray-600'}`}>
                          {patient.status}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={7} className="h-24 text-center text-gray-500 font-medium">
                      No patients matching the selected filter. Great job!
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
