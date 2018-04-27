import { Component, OnInit } from '@angular/core';
import { WorkflowService } from "../workflow.service";


@Component({
  selector: 'app-workflow-list',
  templateUrl: './workflow-list.component.html',
  styleUrls: ['./workflow-list.component.sass']
})
export class WorkflowListComponent implements OnInit {

  workflows = [];

  constructor(private workflowService: WorkflowService) { }

  ngOnInit() {
    this.workflowService.getWorkflows()
      .subscribe(
      workflows => this.workflows = workflows
    );
  }

}
