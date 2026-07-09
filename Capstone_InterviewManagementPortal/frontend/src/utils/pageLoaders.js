import { candidateService } from '../services/candidateService';
import { jobService } from '../services/jobService';
import { userService } from '../services/userService';
import { interviewService } from '../services/interviewService';

export const loadCandidateDetails = (id, signal) => candidateService.getCandidateById(id, { signal });
export const loadCandidateResume = (id, signal) => candidateService.getResume(id, { signal });
export const loadCandidateStatusHistory = (id, signal) =>
    Promise.all([
        candidateService.getCandidateById(id, { signal }),
        candidateService.getCandidateStatusHistory(id, { signal }).catch(() => []),
    ]);

export const loadCandidateList = (search, page, limit, signal) =>
    candidateService.getAllCandidates(search, { signal, params: { page, limit } });

export const loadJobList = (search, page, limit, signal) =>
    jobService.getAllJobs(search, { signal, params: { page, limit } });

export const loadJobDetails = (id, signal) => jobService.getJobById(id, { signal });

export const loadUserList = (search, page, limit, signal) =>
    userService.getAllUsers(search, { signal, params: { page, limit } });

export const loadUserDetails = (id, signal) => userService.getUserById(id, { signal });

export const loadInterviewList = (search, page, limit, signal) =>
    interviewService.getAllInterviews(search, { signal, params: { page, limit } });

export const loadInterviewDetails = (id, signal) => interviewService.getInterviewById(id, { signal });
export const loadAssignedInterviews = (signal) => interviewService.getAssignedInterviews({ signal, params: { page: 1, limit: 100 } });

export const loadDashboardStats = (role, signal) => {
    if (role === 'INTERVIEWER') {
        return interviewService.getInterviewerDashboard({ signal });
    }
    if (role === 'ADMIN') {
        return interviewService.getAdminDashboard({ signal });
    }
    return interviewService.getHrDashboard({ signal });
};

export const loadInterviewFeedbackForm = async (id, signal) => {
    const [interviewData, feedbackData] = await Promise.all([
        interviewService.getInterviewById(id, { signal }),
        interviewService.getFeedback(id, { signal }).catch(() => null),
    ]);
    return { interviewData, feedbackData };
};
