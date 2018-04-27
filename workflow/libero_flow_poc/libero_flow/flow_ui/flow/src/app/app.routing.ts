import { Routes, RouterModule } from "@angular/router";
import { WorkflowListComponent } from "./workflow-list/workflow-list.component";
import { WorkflowDetailComponent } from "./workflow-detail/workflow-detail.component";


const APP_ROUTES: Routes = [
  { path: '', redirectTo: 'workflows', pathMatch: 'full' },
  { path: 'workflows', component: WorkflowListComponent},
  { path: 'workflow/:workflowId', component: WorkflowDetailComponent},
  { path: '**', component: WorkflowListComponent}
];

export const routing = RouterModule.forRoot(APP_ROUTES);
