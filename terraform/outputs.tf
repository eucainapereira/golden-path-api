output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "region" {
  description = "AWS region"
  value       = var.region
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "load_balancer_hostname" {
  description = "The hostname of the LoadBalancer"
  value       = kubernetes_service.api_svc.status[0].load_balancer[0].ingress[0].hostname
}

output "frontend_url" {
  description = "The URL of the static frontend website"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

