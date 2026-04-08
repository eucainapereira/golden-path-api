resource "kubernetes_namespace" "app" {
  metadata {
    name = "golden-path-app"
  }
}

resource "kubernetes_deployment" "api" {
  metadata {
    name      = "golden-path-api"
    namespace = kubernetes_namespace.app.metadata[0].name
    labels = {
      app = "golden-path-api"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "golden-path-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "golden-path-api"
        }
      }

      spec {
        container {
          image = "ghcr.io/your-username/golden-path-api:latest" # Updated via CI/CD
          name  = "api"

          port {
            container_port = 8000
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_svc" {
  metadata {
    name      = "golden-path-api-service"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.api.spec[0].template[0].metadata[0].labels.app
    }

    port {
      port        = 80
      target_port = 8000
    }

    type = "LoadBalancer"
  }
}
