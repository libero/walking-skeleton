<?php

namespace Libero\ApiDummy\Controller;

use Symfony\Component\HttpFoundation\BinaryFileResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use const GLOB_ONLYDIR;
use function is_dir;

final class ArticleController
{
    private $dataPath;

    public function __construct(string $dataPath)
    {
        $this->dataPath = $dataPath;
    }

    public function __invoke(Request $request, string $id, $version, string $part) : Response
    {
        if (!is_dir($articlePath = "{$this->dataPath}/articles/{$id}")) {
            throw new NotFoundHttpException("Article {$id} not found");
        }

        if ('latest' === $version) {
            $availableVersions = array_map('basename', glob("{$articlePath}/*", GLOB_ONLYDIR));
            $version = max($availableVersions);
        } else {
            $version = (int) $version;
        }

        if (!is_dir($articlePath = "{$this->dataPath}/articles/{$id}")) {
            throw new NotFoundHttpException("Article {$id} not found");
        }
        if (!is_dir($articleVersionPath = "{$articlePath}/{$version}")) {
            throw new NotFoundHttpException("Article version {$version} not found");
        }

        $availableLanguages = array_map('basename', array_map('dirname', glob("{$articleVersionPath}/*/{$part}.xml")));
        $language = $request->getPreferredLanguage($availableLanguages);

        return new BinaryFileResponse("{$articleVersionPath}/{$language}/{$part}.xml");
    }
}
